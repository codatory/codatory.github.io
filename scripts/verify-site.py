import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

SITE = "https://www.codatory.page"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
POST = re.compile(r"/(?:[^/]+/)?\d{4}/\d{2}/\d{2}/[^/]+\.html")
SCRIPTS = re.compile(r"<\s*script\b", re.IGNORECASE)


def check(condition, message):
    if not condition:
        raise SystemExit(message)


class Page(HTMLParser):
    def __init__(self, path, markup):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.candidates = []
        self.feed_links = []
        self.canonicals = []
        self.headings = 0
        self.feed(markup)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        check(tag != "script" and not any(name.startswith("on") for name in attrs),
              f"{self.path}: executable markup in <{tag}>")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if value:
                check(not value.strip().lower().startswith("javascript:"), f"{self.path}: {value}")
                self.links.append(value)
        if tag == "source" and attrs.get("srcset"):
            self.candidates.extend(item.split()[0] for item in attrs["srcset"].split(","))
        if tag == "link" and attrs.get("type") == "application/atom+xml":
            self.feed_links.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference-archive", type=Path)
    parser.add_argument("--reference-feed", type=Path)
    args = parser.parse_args()
    output = args.output
    routes = json.loads(Path(__file__).with_name("legacy-routes.json").read_text(encoding="utf-8"))
    pages = {file.relative_to(output).as_posix(): Page(file, file.read_text(encoding="utf-8"))
             for file in output.rglob("*.html")}
    check(pages, "No HTML files found")
    check(not any(output.rglob("*.js")) and not any(output.rglob("*.mjs")),
          "JavaScript files were published")

    def resolve(route):
        path = unquote(route).lstrip("/")
        if path and not path.endswith("/"):
            for candidate in (path, path + ".html"):
                if (output / candidate).is_file():
                    return candidate
            path += "/"
        candidate = path + "index.html"
        return candidate if (output / candidate).is_file() else None

    for route, ids in routes.items():
        file = resolve(route)
        check(file in pages, f"Missing legacy route {route}")
        check(set(ids) <= pages[file].ids, f"{route}: missing heading anchors {set(ids) - pages[file].ids}")
        if POST.fullmatch(route):
            check(pages[file].canonicals == [SITE + route], f"{route}: incorrect canonical")

    for file, page in pages.items():
        if file != "posts/index.html":
            check(page.headings == 1, f"{file}: expected one main heading")
            check(page.feed_links == [SITE + "/feed.xml"], f"{file}: missing Atom discovery")
        for link in page.links + page.candidates:
            url = urlsplit(urljoin(SITE + "/" + file, link))
            if url.netloc != urlsplit(SITE).netloc:
                continue
            target = resolve(url.path)
            check(target is not None, f"{file}: missing local target {link}")
            if url.fragment and target in pages:
                check(unquote(url.fragment) in pages[target].ids, f"{file}: missing fragment {link}")

    archive_links = set(pages["posts.html"].links)
    legacy_posts = {route for route in routes if POST.fullmatch(route)}
    check(legacy_posts <= archive_links, "Archive is missing legacy post links")
    check("/posts.html" in pages["posts/index.html"].links, "Archive alias lost its fallback link")
    if args.reference_archive:
        reference = Page(args.reference_archive, args.reference_archive.read_text(encoding="utf-8"))
        expected_order = [link for link in reference.links if POST.fullmatch(link)]
        actual_order = [link for link in pages["posts.html"].links if POST.fullmatch(link)]
        check(actual_order == expected_order, "Post archive ordering differs from live archive")

    def feed_entries(path):
        feed = ElementTree.parse(path).getroot()
        check(feed.tag == f"{{{ATOM['a']}}}feed", f"{path}: expected an Atom feed")
        check(feed.findtext("a:id", namespaces=ATOM) == SITE + "/feed.xml", f"{path}: feed ID changed")
        check(any(link.get("rel") == "self" and link.get("href") == SITE + "/feed.xml"
                  for link in feed.findall("a:link", ATOM)), f"{path}: missing feed self link")
        return feed.findall("a:entry", ATOM)

    def entry_signature(entry):
        link = next(link.get("href") for link in entry.findall("a:link", ATOM)
                    if link.get("rel") == "alternate")
        return (entry.findtext("a:id", namespaces=ATOM), link,
                entry.findtext("a:published", namespaces=ATOM),
                entry.findtext("a:updated", namespaces=ATOM))

    feed_path = output / "feed.xml"
    entries = feed_entries(feed_path)
    check(len(entries) == min(10, sum(bool(POST.fullmatch(link)) for link in archive_links)),
          "Unexpected number of Atom entries")
    signatures = [entry_signature(entry) for entry in entries]
    check(len(set(entry[0] for entry in signatures)) == len(entries), "Duplicate Atom IDs")
    for entry, (entry_id, link, published, updated) in zip(entries, signatures):
        route = urlsplit(link).path
        check(link == SITE + route and route in archive_links and resolve(route) in pages,
              f"Broken Atom entry link {link}")
        check(entry_id == link.removesuffix(".html") and published and updated,
              f"{link}: invalid Atom entry identity or dates")
        content = entry.findtext("a:content", namespaces=ATOM)
        check(bool(content) and not SCRIPTS.search(content), f"{link}: missing or scripted Atom content")
    if args.reference_feed:
        reference = [entry_signature(entry) for entry in feed_entries(args.reference_feed)]
        check(signatures == reference, "Atom entry IDs, links, dates, or ordering differ from live feed")
    print(f"Verified {len(legacy_posts)} legacy post URLs, {len(entries)} Atom entries, "
          f"and {len(pages)} script-free HTML pages")


if __name__ == "__main__":
    main()

---
layout: post
title:  "The State of Email"
date:   2022-04-28 00:00:00 -0500
categories: 
---

I run my own mail server. I'll pause while you recover from that news.

So, why do I do that? Well, I'm a little extra, and I need to. More than that, I
run my own spam filtering. As part of this whole setup, I've ended up becoming a
lot more in-tune with the state of the art and underlying tech that powers spam
filtering across the Internet.

Great, but what am I writing this for? Well, you as a general user of email
might need to know a little bit about what's happening, why it's happening and
what the implications of that are. But first, let me give you the actionable
bit. Domain reputation matters a lot more now than it has in the past. Be sure
you as a sender are responsible for what you send, are subscribed to the
relevant [feedback
loops](https://www.spamresource.com/2016/03/what-is-isp-feedback-loop-fbl.html),
and ensure every mail you send from your domain is [fully
authenticated](https://www.spamresource.com/2022/04/kickbox-blog-email-authentication-series.html).
If recipients want to receive your mail, and your mail is fully authenticated
there's a path for that to happen no matter how you send it.

Modern mail filtering happens in four major components. You have server
configuration and reputation, domain configuration and reputation, message
contents and user interaction. Every modern filtering solution uses a
point-based system where any one violation is unlikely to result in your mail
being rejected, but every infraction will make it harder to get to the inbox.
Let's do a survey of the different components and talk about what you can do to
help.

### Server Configuration

Historically this was the main barrier to getting your mail delivered. You
needed to have matching forward and reverse DNS, a valid HELO name, and you
needed to be sending from an IP address with good reputation. The complexity of
this keeps a lot of people from running mail servers (though, it's honestly not
that complex). And, while it's important to have your server properly
configured, this is no longer the end all and be-all of mail delivery. Several
large providers, for example, use invalid HELO names. In one of the
higher-volume servers I run, I removed a lot of the traditional wisdom
configuration around rate and connection limits because it really doesn't seem
to be relevant these days. Anything above/beyond the basics of server
configuration don't seem to matter now and it's becoming *more approachable* to
run your own server. Well, except for all the domain configuration stuff we're
about to cover :-). This comes as a side-effect of providers making getting
access to a properly configured server trivial.

### Domain Configuration

Are we here already? Hi! Domain configuration is becoming increasingly
important. What do I mean by "Domain Configuration" anyway? Well, that's simply
providing a way for a recipient to verify that an email sent from your domain is
from you. We started accomplishing that with a technology called Sender Policy
Framework (SPF), which is a simple TXT record that lists the servers which are
allowed to send mail for your domain. It's really the bare minimum you should
do, but it's honestly not that useful these days. It's common to see SPF records
that allow hundreds of thousands of IPs to send on your behalf, and with
businesses using dozens of email sending solutions the limitations of SPF are
really becoming problematic. It was a nice try, but it's not going to help you
get to the inbox. You need it as a security measure, but it's not going to be
enough to stop.

Enter DomainKeys Identified Mail. Rather than a loose ACL of IP's this takes a
different approach to verification - cryptography. Each message in its entirety
is signed with a cryptographic signature that can be verified against a public
key accessible over DNS. As a fun fact, many providers are giving you additional
points for DKIM signatures when the public key can be verified using DNSSEC
which extends signature verification through the DNS chain as well. This is a
very good, forgery resistant technique to verify mail from your domain is from
you.

But DKIM and SPF lack any explicit policy or reporting functionality. That's
where DMARC comes in. DMARC is a simple record that indicates what your domain's
policy is for SPF and DKIM and provides a mechanism to get reports back on your
alignment with that policy. There exist plenty of tools to help you configure
and analyze this record, and the presence of this record makes the work you did
on SPF and DKIM significantly more valuable as a recipient can then verify that
you *intend* mail to be SPF/DKIM authenticated.

DKIM/DMARC do include some inherent complexities that effectively end up with
you absorbing some reputation from senders along the chain and an effective end
to email forwarding across administrative areas. Honestly, that's just a price
we're going to have to absorb. Email forwarding is the main reason I ended up
running my own mail server, as I actively receive mail across several domains
and want to only maintain a single mailbox. Organizations that provide
forwarding-only email addresses will need to reconsider that strategy, and on
the reputation front well... You're only as good as the company you keep.

Once your mail is properly authenticated, you should start building domain
reputation and having better luck at getting to the inbox. Especially for mail
delivered via lower reputation intermediaries.

### Mail Content

If you don't have domain reputation, then your mail is going to be filtered
heavily based on its contents. This is a real problem as a sender because these
rules are... wild. They're machine generated based on input from user
interaction/reports and spam traps, with the occasional rule built by someone
working an abuse desk trying to figure out why they're getting a bunch of manual
reports. Another type of content detection is message hash detection, where a
mail sent in volume to a number of recipients is detected. Each mail system will
have a different mix of detections and points, so you really don't want to be
relying on this system for your mail getting to the inbox. The best
recommendation I can give you here is just to send mail your users want and
don't do a bunch of crazy stuff. Also, apologies in advance if you do genuinely
sell Viagra or similar that's going to be an uphill battle :-).

### User Interaction

If users don't open your email, mailbox providers will stop delivering it. If
users interact with your email (click links, reply, etc) they will be more
likely to deliver it to more people. If users report your message as spam,
mailbox providers will be less inclined to deliver it. Unfortunately, that means
you shouldn't send emails with the entire message in the subject line. It also
gets back to the only practical advice I have for you here as well: send mail
your users want.

## Bonus Content
### Block Lists

If you run mail servers or have hosted mail servers with static IP's, check your
servers against the common block lists. You can do this manually with a tool
like MultiRBL or you can subscribe to a service like
[HetrixTools](https://hetrixtools.com/blacklist-monitor/) to do this
automatically. Do the same for the domains you send from.

### Recipient Configuration

If you use a 3rd party mail filtering solution, be sure it's configured
appropriately for your mailbox solution. Better options exist now that reach
into the mailbox provider and provide filtering after delivery if you aren't
happy with the solution provided by your mail provider.

Well, that's a lot of information for now. If you have further questions or
comments [reach out](https://codatory.com/contact), you might inspire a
follow-up post.

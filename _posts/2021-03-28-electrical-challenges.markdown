---
layout: post
title:  "Electrical Challenges"
date:   2021-03-28 00:00:00 -0500
categories: 
---

Back in [Starting Electrical](https://codatory.com/starting-electrical/), I
wrote about a simple solution to getting some power deployed in my van. This was
excellent, as it gave me the ability to practically measure how I really used
power with some test trips.

What I discovered was what I needed wasn't necessarily a massive battery bank,
but the ability to efficiently *use* that bank. This efficiency comes in three
parts. In this post, I'll discuss the challenges that came from the portable
battery solution.

### Part One: Efficient Usage

Most of these "Solar Generator" devices have an internal Lithium battery that
operates at a voltage different from the ones you use on the front panel. Often
this is 56 volts, but many others are popular as well. That means even highly
efficient 12v appliances will be subjected to the voltage regulation circuitry
of the pack. For most practical uses of these devices, that's fine. But for my
application, that meant I would *never *see a battery life longer than about 12
hours.

### Part Two: Efficient Charging

The particular packs I chose, although this is pretty common across the market,
have a very slow charging rate. Ultimately, in a vehichle the fastest charge
rate you're going to see for a portable device is about 120 watts but that
number is often a lot closer to 40-60 watts. That means to charge the packs I
had used for 12 hours and were now depleted would take over 6 hours of
driving!

### Part Three: Convenience

Most products in this market, due to their standby current usage, disable their
ports once current draw is below a certain threshold for a period of time. That
meant for my main critical load, the fridge, it would power off once the
thermostat satisfied and never power back up. That meant I had to monitor the
pack and make sure it was getting powered back up, and try and keep constant
load draws connected even when they weren't required. Additionally, given the
portable nature of the battery pack it was difficult to permanently install any
auxilary chargers, solar panels, etc. so most charging was accomplished by
removing the packs and plugging them in at home. That meant when loading up for
a trip, I had to remember to grab the packs and re-install them into their
respective homes which... I sometimes failed to do.

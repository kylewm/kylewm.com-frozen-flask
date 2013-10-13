---
category = "Programming"
layout = "post"
title = "Is automating common tasks a waste of time?"
abstract = "Is it worthwhile to spend hours tinkering with a build process, when you can really only hope to save yourself a few minutes a week? (I think so)"
tags = [ "automation", "xkcd",]
date = 2013-05-03T00:00:00Z
---


There was an [xkcd recently][] asking the question "How long can you
work on making a routine task more efficient before you're spending more
time than you save?" The point is if you do a task once a month that
takes a few minutes, it's probably not worth it to spend hours making it
marginally more efficient. It's cute and gently pokes fun at all us [yak
shavers][] (of whom I'm sure Randall proudly counts himself one). It
reminded me of one of my favorite Calvin and Hobbeses were they spend
all weekend building a bed-making robot, which is a great success in
that Calvin successfully does not make his bed all weekend.

But I think it's important not to take the concept too seriously, at
least for software developers. Once a task is automated, it can scale
**up** -- a task you do once a month becomes a task your computer can do
once an hour -- and **out** -- once you've automated a task for one
project you can usually fairly easily adapt it to other projects.

Take the example of build automation. I work for a small company that
does a lot of prototypey projects for usually just one user (at first).
The build/release cycle is usually very ad-hoc with a set of written
instructions for what release flags to set, how to build the jar in
eclipse, package it up with config and library files, where to send it,
etc. It just takes a minute to read the instructions and follow them,
and maybe you put up one release a month, so according to the chart
you've got 1 hour to automate it or it's not worthwhile. But that's not
quite true.

First, mistakes are costly, way more than just the time to repackage the
project correctly. I'm sure everyone's left out a config file or a
dependency when packing up a project. Diagnosing and fixing the problem
on the user's machine is a *huge* waste of time, and arguably worse,
it's embarrassing.

Second, if you spend a day perfecting a script for building, testing,
and releasing your application, then suddenly you have opened up the
possibility of hosting it on a continuous integration server, where it
can be built and tested after every check in. Even for very small teams
where integration is not much of an issue, it's still a nice sanity
check. And now that you are building continuously, you can also publish
nightly snapshot releases. Adventurous users or those who need the
latest fixes can get them at any time and give you feedback right away.

Quick plugs. I do mostly JVM development at work, and I've found
[Gradle][] for dependency management and build automation and
[Jenkins][] for continuous integration to be incredibly useful,
beautiful, and well-thought-out tools.

  [xkcd recently]: https://xkcd.com/1205/
  [yak shavers]: http://projects.csail.mit.edu/gsb/old-archive/gsb-archive/gsb2000-02-11.html
  [Gradle]: http://www.gradle.org/
  [Jenkins]: http://jenkins-ci.org/

---
category = "Programming"
layout = "post"
title = "Cobbling together a blog engine with Pelican and Dropbox"
abstract = "A description of how this blog is automatically generated and updated from plain text files in a Dropbox (or Git repository)."
tags = [ "python", "pelican", "blog",]
date = 2013-07-12T00:00:00Z
---


Right now is an interesting time for the web. Spam/popups/unwanted
porn are essentially gone, it's basically safe for children, and most
of the information I want is well-moderated and easily accessible --
my Google searches generally take me to StackOverflow, Wikipedia, or
IMDB (depending on the time of day). Almost anyone I'd like to get in
contact with is on Facebook (except for those few weird holdouts who
have somehow still avoided being "on" the internet, which you can't
help but respect).

Of course all of the organization has come at the cost of proprietary
protocols, walled gardens, and homogenization. I'll stop before I get
all "if you aren't paying for the product, you are the product", but
it was important to me to start a little site:

 1. on a domain that I own, 
 2. server space that I pay money for<sup>*</sup>
 3. that reports "[Ghostery](http://www.ghostery.com/) found 0 trackers".

Unfortunately, while I've gotten to be a much better programmer in the
last decade, my HTML/CSS-fu is stuck in about 1996. I could do
anything with nested `<table>`s but am all but completely lost with
`<div style="clear: both;">`. So my plan was to go as minimal as
possible. I wanted to write posts in Markdown, save them in a Dropbox
folder, and have them formatted and published automatically. There are
a few services that do basically this --
[calepin.co](http://calepin.co) and
[scriptogr.am](http://scriptogr.am) are both nice (but don't host
images and more importantly don't meet #2 above).

Basically all the pieces are already there. I decided to limit myself
to Python<sup>&dagger;</sup> generators, of which [Pelican][] seems to
be far-and-away the most active. So I applied for a Dropbox "app
folder" API key and hacked up a little cron job to poll the app folder
for changes. The Dropbox API has a really nice request for getting
information about which files have changed since the last request:
[DropboxClient.delta][]. If that request comes back empty (which it
will 99.9% of the time) we're done. If some files have been
added/removed/modified, the script syncs up the `content/` folder and
re-runs Pelican. Finally it shells out to lftp which uses `mirror -R
output .` to transmit the changed html files.

The source for this script is up on GitHub [pelican-dropblog][]. It's
not anything resembling robust or secure, but it might be a good
starting point for someone else. The theme is based on the remarkably
lightweight [Skeleton][skeleton] responsive framework, and
fonts/colors (or the lack thereof) were inspired by [Jinja2's
site][jinja].

I feel a little bit like the little kid who spends 2 hours determining
all the parameters and rules of the make-believe world, what powers
they will have, and 5 minutes actually playing (that is to say,
me). When you go researching creative ways to set up a blog, you find
a lot of blogs where the only post is how they set up the blog... but
maybe this one will be different :)

**Update:** my friend [Ethan](http://www.hydrous.net) admonished me
for not version controlling the blog's source, and he was right. I
added a few lines to the script so it can optionally update from a git
repository rather than a dropbox folder. Right now it's still polling
every 5 minutes, but I'm going to look into whether I can have
Travis-CI build/deploy the site with a post-receive hook.

<small> <sup>*</sup> that is, it won't be acqui-hired and shut down by
a competitor &agrave; la Posterous, or squelched because of
competiting interests in the same company (ahem, Reader)

<sup>&dagger;</sup>not because I don't like Ruby but because I'm
daunted by its ecosystem (rake, rbenv) </small>

[Pelican]: http://docs.getpelican.com/en/latest/
[pelican-dropblog]: https://github.com/kylewm/pelican-dropblog
[skeleton]: http://www.getskeleton.com/
[jinja]: http://jinja.pocoo.org/
[DropboxClient.delta]: https://www.dropbox.com/static/developers/dropbox-python-sdk-1.6-docs/index.html#dropbox.client.DropboxClient.delta
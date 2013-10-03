---
layout = "post"
title = "Migrating from Subversion to Mercurial"
abstract = "Notes on migrating a tangled Subversion repository to Mercurial"
date = 2012-12-02T22:30:00Z
tags = [ "mercurial", "subversion", "version control" ]
category = "Programming"
---

**Problem:** Start with a single subversion repository containing many
sub-projects, whose root directories have been moved or renamed since
they were created. Convert this repository to Mercurial,
one-repository-per-project, while maintaining the full history for every
file.

**Solution:** Clone the *entire* Subversion repository to Mercurial. For
each sub-project, use the [hg convert][] extension with the `--filemap`
option to include every name that the project root directory has had, at
the same time renaming the root directories to '.'

If that makes sense, you can stop reading now.

**Unnecessarily Long Explanation:** These days at work we use Mercurial
for most new projects (no reason it couldn't be git either, that's just
the one folks are familiar with), but older code tends to still be in
svn or cvs. For almost a year I have been toying with the idea of
converting my main project (with over 11 years of active development
history) over. I whispered in ears when the server had an outage,
whenever someone wanted to send me a substantial set of changes but was
not ready to commit those changes, and any time I noticed people going
to great lengths to work around shortcomings they didn't even know svn
had. Eventually I wore them down, which left me with a technical
challenge.

As you would expect of a project that's been around that long, there
were some odd features of the version history. Chief among them, two or
three years ago, a naive but well-meaning developer (me) had reorganized
the repository, pulling in the last remaining bits of code from cvs into
the svn repository and moving the sub-projects around to make room.
Prior to the reoganization, the subversion repository was standard
enough.

    REPOSITORY (SubProjectA)
      /trunk
        /dev
          --> Actual project source here <--
        /Documentation
        /Design
      /branches
         --> branches & domain-specific-configurations <--
      /tags

After pulling in the second project:

    REPOSITORY (SubProjectA)
      /trunk
      /branches
      /tags
      /SubProjectB
        /trunk
        /branches
        /tags

And after the reorganization:

    REPOSITORY
      /main
        /trunk
          /SubProjectA
          /SubProjectB
          /Documentation
          /Design
        /branches
        /tags
      /domains
        /Domain1
          /trunk
          /branches
          /tags
        /Domain2
        ...

Fortunately we did *not* have a complicated set of branches that needed
to be maintained. In fact it was only really important that I save the
revision history for two folders: `main/trunk/SubProjectA` and
`main/trunk/SubProjectB`.

Converting the non-standard directory structure would not have been much
of a problem, except that I had done the reoganizaiton the lazy way,
moving directories around haphazardly with `svn mv`. I was able to use
the excellent [hgsubversion][] to clone
`svn://.../main/trunk/SubProjectA` but the history only went back as far
as the reorganization. I tried using `hg convert --splicemap` and also
`hg rebase` to try to stick the missing revision ranges back in, but
even though it created a nice continuous tree, it did not magically put
individual file histories back together. I also tried approaching it
from the Subversion side, hoping to restructure the repositories
properly before converting. svndumpfilter was going to be painful and
maybe impossible, and for reasons I don't quite remember I wasn't able
to get very far with [svndumpfilter3][] either.

**What Finally Worked:** The final solution is sort of obvious in
retrospect -- pull the full history of every file into Mercurial first,
and then use convert to pare down and rename the files. (Sort of on
accident) I cloned the entire monolithic Subversion repository into Hg
one night.

    hg convert svn://server/MonolithicRepository All.hg

Then created filemap-a.txt:

    include trunk/dev
    include trunk/SubProjectA
    include main/trunk/SubProjectA
    rename trunk/dev .
    rename trunk/SubProjectA .
    rename main/trunk/SubProjectA .

and filemap-b.txt

    include SubProjectB/trunk
    include main/trunk/SubProjectB
    rename SubProjectB/trunk .
    rename main/trunk/SubProjectB .

and used it to do Mercurial-to-Mercurial conversions of the All.hg
repository

    hg convert --filemap filemap.a.txt All.hg SubProjectA.hg
    hg convert --filemap filemap.b.txt All.hg SubProjectB.hg

This left me with SubProjectA.hg and SubProjectB.hg with a full and
continuous revision histories for all files.

  [hg convert]: http://mercurial.selenic.com/wiki/ConvertExtension
  [hgsubversion]: mercurial.selenic.com/wiki/HgSubversion
  [svndumpfilter3]: http://furius.ca/pubcode/pub/conf/bin/svndumpfilter3.html

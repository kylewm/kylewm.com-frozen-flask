---
category = "Programming"
layout = "post"
title = "A simple raytracer in Common Lisp"
abstract = "Some renders from a minimal raytracer I wrote as a reintroduction to Common Lisp"
tags = [ "common lisp", "graphics", "side projects",]
date = 2013-05-07T00:00:00Z
---

A few months ago I wrote [a small, ~350 line, raytracer][github] to [re]teach
myself Common Lisp (SBCL in particular)... Like any good CS major, I
love my Lisps! I had some exposure to Racket (then Scheme) in school and
had recently played around with Clojure, so it seemed only fitting.

The raytracer itself only handles spheres but supports different types
of materials with reflection, refraction, and supersampling. Here is
probably my favorite render, with the progression in more detail below.

![raytrace5](raytrace5.png)

<!--more-->

Mostly I just think this is funny. Ray intersection with two 3D objects
is a really inefficient way to draw two filled circles.

![raytrace1](raytrace1.png)

After I figured out that normals point AWAY from the center of the
sphere, suddenly there was diffuse shading!

![raytrace2](raytrace2.png)

And then subtle specular highlights:

![raytrace3](raytrace3.png)

A little less subtle. The problem with the color of the shadow is more
pronounced here but I think is visible on the previous three renders. I
think what was going on there was that the shadow ray was intersecting
the object itself -- adding a small epsilon value before the next
version fixed it.

![raytrace4](raytrace4.png)

Here they are with reflection (and supersampling, which was almost no
additional code at all but made a huge difference in the quality of the
images, especially smoothing out the shadows)

![raytrace5](raytrace5.png)

And finally refraction!

![raytrace6](raytrace6.png)

At this point I sort of ran out of steam, but it was a super fun
project, and I was happy with it as a proof-of-concept. I was impressed
with CL's expressiveness and speed. I mostly write Java for work, and
it's such a nice change of pace to use a language whose designers
*trusted* you the developer not to do stupid stuff ... where "missing"
features can be added.

But I can definitely see where lack of libraries could be problematic
(my understanding is that this is why spez switched from CL to Python
after prototyping Reddit). For example, I could not really find a
sanctioned GUI library, just thin wrappers around the usual suspects.
The accepted suggestion on StackOverflow was to just write web apps.

  [github]: https://github.com/kylewm/cl-raytrace


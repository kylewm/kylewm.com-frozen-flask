---
category = "Programming"
layout = "post"
title = "Writing a simple maven plugin"
abstract = "My first foray into writing a plugin for Maven. My example plugin invokes CMake in a subprocess."
tags = [ "cmake", "maven",]
date = 2012-12-08T00:00:00Z
---


It took a year and a half of using it, but I think I finally "get"
[Maven][]. I tried over and over to use it as Ant with dependency
management... forcing it to do what I wanted it to do by cobbling together
profiles and `maven-exec-plugin` executions. But a pom is a
configuration file not an executable script. I have finally learned to
stop treating it like one.

Here's what changed: I learned how easy it is to write plugins. I'd
always imagined plugin authoring would have a high learning curve, that
it wouldn't be worth the time investment, and that I would be awash in
XML. It turns out the plugin mechanism is gloriously simple. You can
learn how to write one and write one in way less time than it takes to
put together your collection of found plugins to do some non-standard
procedure.

So I'm working on a project that mixes Java and C++. The Java code
builds with Maven, and the C++ has recently been outfitted with a CMake
[CMake][] (an absolute joy, by the way) configuration. I want Maven to
delegate to CMake, and then to pack up the resulting library in a zip
file.

Maven's [Guide to Developing Java Plugins][] is really good. I won't try
to reproduce it here, but here was my experience. Use the
`maven-archetype-plugin` to generate a skeleton project:

    :::bash
    mvn archetype:generate  
      -DgroupId=com.hypothetical  
      -DartifactId=build-with-cmake-maven-plugin  
      -DarchetypeGroupId=org.apache.maven.archetypes  
      -DarchetypeArtifactId=maven-archetype-mojo  
      
This sets up a project with one deceptively simple mojo. -- it has
examples of all the annotations and methods I needed to write a basic
plugin. I wanted two goals, `build` and `clean`, so I copied MyMojo to
BuildWithCMakeMojo, changed the goal to `build` and the phase to
`compile` (to use a custom plugin, you always have to specify the goal
in your pom, but you do not have to specify a phase if one is defined by
the plugin).

Maven reads most of the metadata about your plugin from Javadoc
annotations (I believe there are Java 5-style annotations available now
too, but they weren't in the tutorial). Here is the header comment:

    :::java
    /**  
     * @goal build  
     * @phase compile  
     */  
    public class BuildWithCMakeMojo extends AbstractMojo {

I added a few parameters to the Mojo by adding private class members,
annotated with `@parameter`. The first parameter (baseDir) is also
annotated with `@readonly`. This means it's not user-configurable -- it's
just a way to pass the value from Maven into my plugin. Like magic, it
treats Strings like Strings, Files likes Files, and Dates like Dates,
and numbers like numbers. I'm often frustrated with how rigid Java is,
but this stuff is cool. Reflection + annotation is one area where you
can have a little fun; I'm going to it more and more to get rid of
repetition and boilerplate in my own code.

    :::java
    /**  
     * @parameter expression="${basedir}"  
     * @readonly  
     */  
    private File baseDir;

    /**  
     * Directory for the out of source build  
     * @parameter  
     */  
    private File buildDirectory;

    /**  
     * Architecture. One of { "x86", "x64" }  
     * @parameter default-value="x86"  
     * @required  
     */  
    private String archPrefix;

    /**  
     * OS. One of { "win", "linux" }  
     * @parameter default-value="win"  
     * @required  
     */  
    private String osPrefix;  


I added a little bit of logic to determine choose the CMake generator
based on the arch and os:

    :::java
    String generator;  
    if ("win".equals(osPrefix)) {  
        generator = "Visual Studio 9 2008";  
        if ("x64".equals(archPrefix)) {  
            generator += " Win64";  
        }  
    }  
    else if ("linux".equals(osPrefix)) {  
        generator = "Unix Makefiles";  
    }  
    else {  
        throw new MojoExecutionException("Unsupported OS: " + osPrefix);  
    }

but mostly the rest is just shelling out to cmake. Java is not the
loveliest language for writing what is basically a shell script, but it
works (Well mostly. For `clean`, I just wanted to `rm -rf` the build
directory, but there didn't appear to be an easy way to do that safely,
so I punted for now).

Here is a [gist with the full listing for BuildWithCMake][].

*Quick CMake tip:* Tutorials typically tell you to use `cmake` to
generate Makefiles and then `make` to build them. I needed to build my
library on both Linux and Windows (Visual C++) so on the latter I was
calling `cmake` to generate and `devenv /Build`. This meant I had to
*find* Visual Studio and then issue different build and clean commands
dependening on the platform. Silly me, it turns out cmake has a command
line argument to do all of this for you. In the build directory:

    :::bash
    cmake --build . --target install  
    cmake --build . --target clean

Delegates to devenv on a VS project and make on a Unix Makefiles
project.

Once I figured this out, I realized all my needs would've been met with
an existing CMake plugin [like this one][] but the lesson was already
learned and the damage was already done.

  [Maven]: http://maven.apache.org
  [CMake]: http://www.cmake.org/
  [Guide to Developing Java Plugins]: http://maven.apache.org/guides/plugin/guide-java-plugin-development.html
  [gist with the full listing for BuildWithCMake]: https://gist.github.com/4248372
  [like this one]: http://code.google.com/p/cmake-maven-project/

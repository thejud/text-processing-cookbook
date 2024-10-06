# An Introduction

In my daily work, I often have a need to quickly analyze textual data from
logfiles, APIs and console commands. I need to answer questions like how many
events occurred, how frequently they occurred, and/or how they relate to other
events over a period of time.

Many of my data processing tasks follow this pattern:

* FILTER the input, selecting a set of lines that I want
* EXTRACT/TRANSFORM the selected lines into a more useful format
* AGGREGATE the data to summarize

Due to the power and flexibility of linux pipes, I can quickly assemble a set
of commands that are very effective on small to medium sized datasets (able to
fit on a single machine). Without doing a lot of programming, I can do
exploratory analysis, and answer many types of questions quickly.

For example, sometime I want to print the last field in a series of lines
that match the pattern "DEBUG". `awk` is *one* way to do this:

```
grep "DEBUG" myfile | awk '{print $NF}'
```
See [the recipe](project:extraction.md#printing-the-last-column-awk-and-perl)

I try to remember a set of techniques that I can put together on the fly to
answer questions in under 60 seconds, often much less. More complicated
questions can be answered via an actual program, or with higher-level tools.

This document describes a variety of linux tools (standard and/or open source)
that I have found useful for various parts of the process. They are also tools
and techniques that I find myself re-discovering periodically, so this document
is both a reminder to myself about things that have worked for me, and
potentially a teaching tool for others. Note that there are multiple approaches
to almost every recipe I've listed here.

Conventions: In code blocks, the command is left justified, while output from
the command is indented by one space. I find it annoying to remove the "$ "
prefix from commands when copying and pasting from a page. 

I also use the `cat foo | bar` form in many places rather than `bar < foo`
because I've fat-fingered '>' instead of '<' one too many times, overwriting my
source file. Additionally, I also use most of these scripts as part of a larger
pipeline, so there's often another few steps to generate the input instead of a
simple `cat` command. Here's an example of how a command and its output will be
formatted.

    seq 10 | head -3
     1
     2
     3

Finally, unless otherwise noted, the commands should handle more than one line
of input even if I only provide one line of input, e.g. 
`echo foo,bar,baz | csvlook -H`.

## Other Resources

There's a great list of text processing utilities here:

  * [structured text tools](https://github.com/dbohdan/structured-text-tools)

Jeroen Janssens wrote a good book about this topic

  * [data science at the command line book](https://www.datascienceatthecommandline.com/)

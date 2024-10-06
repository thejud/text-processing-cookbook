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


Here is a reasonably complex example:

On a project, a coworker asked what dates were available to analyze
in a machine learning project. The data had been collected into S3, grouped
by event class, user, and date. As I knew where the data was stored in S3,
I was able to quickly list the files using an `s3 ls --recursive` command
and store that in a file for quick summarization.

The S3 output was a list of several hundred files approximately like below.
Each line has a creation data, a size, and then the file path that encodes:

- an event class
- a user id
- a date
- the actual filename

```
2024-09-22 139769207 data/class=3002/user=aaa/date=2024-09-21/part-00005
2024-10-04   8235665 data/class=1007/user=aaa/date=2024-10-03/part-00009
2024-10-04     26936 data/class=103006/user=bbb/date=2024-10-03/part-00008
2024-09-13  92385199 data/class=1010/user=aaa/date=2024-09-12/part-00003
2024-10-03  51873127 data/class=1007/user=aaa/date=2024-10-02/part-00001
2024-09-10     52364 data/class=3001/user=aaa/date=2024-09-09/part-00003
2024-09-11  53877463 data/class=1007/user=aaa/date=2024-09-10/part-00001
2024-10-05  36197597 data/class=1007/user=bbb/date=2024-10-04/part-00005
2024-09-14     54249 data/class=103006/user=aaa/date=2024-09-13/part-00000
2024-09-03 146174053 data/class=3002/user=aaa/date=2024-09-02/part-00001
```

I wanted to see the first and last dates available, and have a rough idea if
there were any big gaps by counting the number of dates between the first and last.

Here's the abbreviated output, with the user, event class, first and last date and count of files.

```
user=aaa  class=1007    date=2024-09-05  date=2024-10-05  31
user=aaa  class=3001    date=2024-08-25  date=2024-10-05  42
user=aaa  class=3002    date=2024-08-25  date=2024-10-05  42
user=bbb  class=1007    date=2024-09-30  date=2024-10-05  6
user=bbb  class=3001    date=2024-09-25  date=2024-10-05  11
user=bbb  class=3002    date=2024-09-25  date=2024-10-04  10
```

and here is the transformation I used to summarize the data:

```shell
cat /tmp/files 
    | awk '{print $NF}' \
    | grep user=
    | perl -pe's/part.*//'  
    | perl -pe's/.*data\///' 
    | tr / '\t'  
    | sort --uniq
    | datamash --group 2,1 first 3 last 3 count 3
    | column -t
```

See the recipe [Find available data by user, event class and date](project:solutions.md#find-available-data-by-user-event-class-and-date)

If you look at this and think, "I could do it in fewer steps!" then congratulations! 
I encourage you to poke around a bit and see some of the recipes, as there will likely
be some tools or approaches you haven't tried, or perhaps only forgot!

If you look at this, and think, that's really cool, but WTF just happened, then
keep reading. Each of these steps has at least one recipe. While it has taken
me a long time to get to this point, I was able to summarize the data in a
minute or two by combining "simple" steps and progressively refining the results
until I got what I wanted.

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
source file. Additionally, I use most of these scripts as part of a larger
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

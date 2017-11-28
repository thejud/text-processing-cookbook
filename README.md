# text-processing-cookbook

A cookbook of tools and techniques for processing text and data at the linux
command line by Jud Dagnall <https://github.com/thejud/text-processing-cookbook>

Table of Contents
=================

* [text\-processing\-cookbook](#text-processing-cookbook)
  * [Overview](#overview)
  * [FILTER AND SELECT](#filter-and-select)
    * [ag \- the silver searcher](#ag---the-silver-searcher)
    * [searching via perl](#searching-via-perl)
      * [select first and last lines](#select-first-and-last-lines)
    * [range selection with perl's flip\-flop (\.\.) operator](#range-selection-with-perls-flip-flop--operator)
  * [EXTRACTION](#extraction)
    * [Extracting one or more columns with awk](#extracting-one-or-more-columns-with-awk)
    * [Extract simple fields via cut](#extract-simple-fields-via-cut)
    * [Extract by character position with cut](#extract-by-character-position-with-cut)
    * [Extract fixed\-width fields with awk](#extract-fixed-width-fields-with-awk)
    * [Extract fixed\-width fields with in2csv](#extract-fixed-width-fields-with-in2csv)
    * [Convert whitespace\-delimited columns to csv](#convert-whitespace-delimited-columns-to-csv)
    * [cutting columns, other tools](#cutting-columns-other-tools)
    * [f \- trivial field extractor](#f---trivial-field-extractor)
    * [scut \- swiss army knife of column cutters](#scut---swiss-army-knife-of-column-cutters)
    * [to extract columns from CSV data, use csvcut](#to-extract-columns-from-csv-data-use-csvcut)
  * [TRANSFORMATION](#transformation)
    * [General transformation with perl \-pE and \-nE](#general-transformation-with-perl--pe-and--ne)
    * [Create several simple filters rather than one complicated ones](#create-several-simple-filters-rather-than-one-complicated-ones)
    * [collapse or replace spaces and newlines](#collapse-or-replace-spaces-and-newlines)
    * [convert spaces to newline with tr or perl](#convert-spaces-to-newline-with-tr-or-perl)
    * [remove newlines with perl](#remove-newlines-with-perl)
    * [reshape text with rs](#reshape-text-with-rs)
    * [merge sort  multiple files of sorted data](#merge-sort--multiple-files-of-sorted-data)
    * [paste: add files side by side](#paste-add-files-side-by-side)
    * [join: intersect two files](#join-intersect-two-files)
    * [Concatenate files, skipping header line](#concatenate-files-skipping-header-line)
    * [Remove the first n lines of a file with tail](#remove-the-first-n-lines-of-a-file-with-tail)
    * [Sort a file with a header](#sort-a-file-with-a-header)
    * [put data into a specific number of columns with pr](#put-data-into-a-specific-number-of-columns-with-pr)
    * [making data tables with column](#making-data-tables-with-column)
    * [Use column to create a flexible number of columns to fill the width\.](#use-column-to-create-a-flexible-number-of-columns-to-fill-the-width)
    * [joining all lines with xargs](#joining-all-lines-with-xargs)
  * [Grouping data](#grouping-data)
    * [Find distinct items, removing duplicates](#find-distinct-items-removing-duplicates)
    * [Find unique items](#find-unique-items)
    * [Find duplicate items](#find-duplicate-items)
    * [Find lines that are in one file, but not in another](#find-lines-that-are-in-one-file-but-not-in-another)
    * [Split data into files based on a field](#split-data-into-files-based-on-a-field)
  * [Frequency counts and distributions](#frequency-counts-and-distributions)
    * [get a frequency count of items, or find common items](#get-a-frequency-count-of-items-or-find-common-items)
    * [Find the n most common items](#find-the-n-most-common-items)
    * [Better frequency counts](#better-frequency-counts)
    * [Histogram of values](#histogram-of-values)
  * [SPECIALIZED TOOLS FOR AGGREGATION, SUMMARY, ANALYSIS AND REPORTING](#specialized-tools-for-aggregation-summary-analysis-and-reporting)
    * [stats](#stats)
    * [csvstat](#csvstat)
    * [datamash](#datamash)
      * [quick grouped stats with datamash](#quick-grouped-stats-with-datamash)
      * [Cross tables/pivot tables with datamash](#cross-tablespivot-tables-with-datamash)
  * [csv/tsv:](#csvtsv)
    * [csvkit](#csvkit)
  * [json](#json)
    * [jq](#jq)
  * [Generating data](#generating-data)
    * [Generating columns of data by column](#generating-columns-of-data-by-column)
    * [Generating columns of data by row](#generating-columns-of-data-by-row)
    * [Generating a sequence of letters:](#generating-a-sequence-of-letters)
    * [Generating random numbers](#generating-random-numbers)
      * [jot](#jot)
    * [Generating permutations with shuf](#generating-permutations-with-shuf)
  * [Sorting](#sorting)
    * [gnusort on osx via coreutils](#gnusort-on-osx-via-coreutils)
      * [sort items lexicographically, numerically (gnu sort)](#sort-items-lexicographically-numerically-gnu-sort)
      * [sort with size units, (k, m, etc)](#sort-with-size-units-k-m-etc)
  * [Batch and parallel execution with xargs and parallel](#batch-and-parallel-execution-with-xargs-and-parallel)
    * [xargs](#xargs)
    * [GNU parallel](#gnu-parallel)
  * [Misc](#misc)
    * [Progress bars in pipes](#progress-bars-in-pipes)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

Rebuild with :

    gh-md-toc README.md

## Overview

I often find myelf processing text files on the linux command line, things like, logfiles, data
files, command output, etc... 

Many of my data processing tasks follow this pattern:

* FILTER the input, selecting a set of lines that I want
* EXTRACT/TRANSFORM the selected lines into a more useful format
* AGGREGATE the data
* REPEAT

Due to the power and flexibility of linux pipes, I can quickly assemble a set
of commands that are very effective on small to medium sized datasets (able to
fit on a single machine). Without doing a lot of programming, I can do
exploratory analysis, and answer many types of questions quickly.

I try to remember a set of techniques that I can put together on the fly to
answer questions in under 60 seconds, often much less. More complicated
questions can be answered in an actual program, or with higher-level tools.

This document describes a variety of linux tools (standard and/or open source)
that I've found useful for various parts of the process. They are also tools
and techniques that I find myself re-discovering periodically, so this document
is both a reminder to myself about things that have worked for me, and a
potentially teaching tool for others. Note that there are multiple approaches
to almost every recipe I've listed here.


Conventions: In code blocks, the command is left justified, while output from
the command is indented by one space. I find it annoying to remove the "$ "
prefix from commands when copying and pasting from a page. 

I also use the `cat foo | bar` form in many places rather than `bar < foo`
because I've fat-fingered '>' instead of '<' one too many times, overwriting my
source file. Additionally, I also use most of these scripts as part of a larger
pipeline, so there's often another step. Here's an example of how a command and
its output will be formatted.

    seq 10 | head -3
     1
     2
     3

Finally, unless otherwise noted, the commands should handle more than one line
of input even I only provide one line of input, e.g. 
`echo foo,bar,baz | csvlook -H`.

## FILTER AND SELECT

grep is the linux go-to search tool, supporting fast searching using patterns
and regular expression.

I'll cover some other options here, and assume a basic understanding of grep
and regular expressions going forward.

### ag - the silver searcher

[ag - AKA the silver searcher](https://github.com/ggreer/the_silver_searcher) is
a fast, flexible grep alternative to grep forcused on powerful searches with
perl-compatible regular expressions and common default options like recursive
search, avoiding .git files, and a few other nice features.

`brew install the_silver_searcher` or `apt-get install silversearcher-ag`

### searching via perl

perl also has build in regular expressions, and a few other things that make it worthwhile.

#### select first and last lines

Found this recently: https://unix.stackexchange.com/a/139199

    seq 10 |  perl -ne 'print if 1..1 or eof'

It's worthwhile because it demonstrates some quirky perl features that are quite useful:

`eof` is the end of the file, and is relatively self explanatory. What is interesting is that you can print
the last line once eof is detected.

The flip-flop operator is the `1..1` portion, is true starting on the first line only.

### range selection with perl's flip-flop (..) operator

Perl has an interesting operator called the flip-flop operator that can be used to select ranges of things.

    echo "a b c d e f g" | tr ' ' "\n" | tee letters
     a
     b
     c
     d
     e
     f
     g

Now, select everything between the line starting with c, and the line starting with e:

    perl -nE'print if /^c/../^e/' letters
     c
     d
     e

If integers are provided for one or both conditions, it is matched against the line number (AKA $.)

    perl -nE'print if /^c/..5' letters
     c
     d
     e

    perl -nE'print if 3..5' letters
     c
     d
     e

And finally, you can continue to the end of the file by using eof:

    perl -nE'print if /^e/..eof' letters
     e
     f
     g
     


once whatever is on the left side of the `..` is matched, the entire expression becomes true. It becomes false
after the right side is matched. Often, regexes are used on each side, e.g. `print if /^START/../^END/` to
print all lines between started and ended.

 
## EXTRACTION

Extraction is a subset of transformation, but it is important enough to have
its own section.

perl, sed and awk are all common tools for both selection and extraction

### Extracting one or more columns with awk

one trivial but common use of awk is to extract one or more columns from text
with variable whitespace, like formatted text or the output of a command like
ls:

    ls -l | tail +2 | awk '{print $5}'

### Extract simple fields via cut

cut is designed to extract fields from a line, given a single character
delimter or position list. It will not split on patterns or multi-chararacter
delimiters. Use one of the tools described below if you have more complicated
data.

    cat > data <<EOF	
    foo:bar:baz
    fun:stuff:today
    EOF

    cat data | cut -d: -f 1,3
    foo:baz
    fun:today

Note that cut apparently ignores field order:

    cat data | cut -d: -f 3,1
    foo:baz
    fun:today


### Extract by character position with cut

    cat > alpha <<EOF
     abcdef
     gehijk
     EOF

    cat alpha | cut -c '2-4,6'
     bcdf
     ehik

### Extract fixed-width fields with awk

Sometimes you will have fields of known (but possibly variable) width, AKA
fixed width format.

awk can be used to extract the fields (you may need to install gnu awk).
Found via https://stackoverflow.com/a/28562381

    echo aaaaBBcccccDe | awk '$1=$1' FIELDWIDTHS='4 2 5 1 1' OFS=, 
    aaaa,BB,ccccc,D,e


The `$1=$1` just forces awk to re-parse each line using the FIELDWIDTHDS you've specified. `OFS` is the output separator.

Note that this recipe gets every field, and every character between each field.
See the cut recipe above, or the in2csv approach if you only part of
each line, or only osme fields.

### Extract fixed-width fields with in2csv 

You can also use `in2csv` (part of `csvkit`) to convert fixed with to csv files
with headers. in2csv requires a schema file, so this is probably most practical
if you find yourself doing this frequently for the same schema, or there are a
LOT of fields and you probably need to iterate through them anyway.

Define a schema file:

    cat > fields.csv <<EOM
     column,start,length
     name,1,4
     id,5,2
     field1,7,5
     section,12,1
     category,13,1
     EOM

And then use the schema file to extract fixed-width fields:

    echo aaaaBBcccccDe | in2csv -s fields.csv
     name,id,field1,section,category
     aaaa,BB,ccccc,D,e

### Convert whitespace-delimited columns to csv

This can be relatively simple. If you know that you data doesn't contain
any additional commas, you can do a simple substitution:

    perl -pe's/\h+/,/g';  # horizontal space, no newline
    perl -anE'say join(",", @F)'

If you can't be sure that there won't be commas in the fields, you'll want to
do proper quoting. Use a real csv tool. Here's a way to convert to tsv:

    perl -anE'say join("\t", @F)' | csvformat -t -H

### cutting columns, other tools

Cutting columns of text is such a common operation that it's worthwhile to have
a few other tools on hand.

### f - trivial field extractor

[f column extractor](https://blog.plover.com/prog/runN.html)

f is a tool with a laser-sharp focus: Extract a single column from a whitespace
delimited file. If you find yourself going often to awk for something like `awk
'{print $3}'`, then add f to your arsenal.


    # quickly extract one column
    printf "the quick brown fox\nand so it goes" | f 3
     brown
     it

### scut - swiss army knife of column cutters

[scut is a better (if slower) cut, extracts arbitrary columns to be selected
based on regexes](https://github.com/hjmangalam/scut)

    # zero indexed, easy to get many columns
    cat data | scut -f '2 1'

    # negative columns are removed
    cat data | scut -f 'ALL -1'

### to extract columns from CSV data, use csvcut

`csvcut` is part of the `csvkit` suite

## TRANSFORMATION

perl is my tool of choice for many line-oriented transformations. It's worth
learning a few tricks, and invensting some time one or more of perl, sed or awk.

### General transformation with perl -pE and -nE

The perl -p option turns on filter mode. Any changes made by the expression
argument (-e or -E) will be applied, and then each line will be printed. Using
regular expressions is a good way to remove parts of the line, or add to it.

Here's an example of removing the subsecond timestamp from a log line:

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -pe's/\.(\d*) / /'  
     2017-11-01T12:14:22 ERROR critical

You can also extract portions of the line by matching against the entire line.
Here's a moderately complicated regular expression that extracts the
hour:minute pair, and the log level (ERROR or FATAL). This might be the first
step in analyzing errors per minute.

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -pe's/^.*?T(\d\d:\d\d):\S+ (ERROR|FATAL) .*$/$1 $2/'
     12:14 ERROR

I tend to prefer to only take the parts I want, rather than replacing the
entire line. perl's `-n` flag loops over all the input, but doesn't print
anything. The -E flag is a modern version of the -e flag, and just makes some
of the more modern perl features available. I use it so that I can use "say"
instead of "print", which is shorter and adds the trailing newline.


    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -nE'/T(\d\d:\d\d):\S+ (ERROR|FATAL)/ and say "$1 $2"'
     12:14 ERROR

If you don't know anything about regular expressions, this will all seem very
mysterious, but if you do much text (or log) munging, it's worthwhile to learn
the basics. 

### Create several simple filters rather than one complicated ones


Like anything other part of your pipeline, it's fine to clean up your
output progressively with multiple smaller, simpler filters. I often do this
because it's easier to apply fixes than to get one large regex just right.
Naturally, if you're building a high-volume or production pipeline, it's
probably worthwhile to take the time to get it right. 

Here's the filter from the previous recipe broken down into several steps.

Note that in this example I'm using tee /dev/stderr to give some diagnostic
output at each stage in the pipeline so you can see how the line is
progressively refined. You would only want to do that for debugging or
development. 

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | cut -d ' ' -f 1,2 \
    | tee /dev/stderr \
    \
    | perl -pe's/^.*?T//' \
    | tee /dev/stderr \
    \
    | perl -pe's/\.\S+//' \
    | tee /dev/stderr \
    \
    | perl -pe's/:\d\d / /'
     2017-11-01T12:14:22.12352 ERROR
     12:14:22.12352 ERROR
     12:14:22 ERROR
     12:14 ERROR


Another advantage of several simple filters is that you don't have to spend
time looking up the particular syntax.

Recently, I've been dealing with billions of records in blocks of 10 million or
so. In the logfiles for these tools, I use numbers with comma separation so
it's a little easier to quickly see the exact magnitude of the numbers.

Here's a partial log line. I typically use key=value format in my log as well,
as they are both clear and easy to parse.

  2017-11-20T15:33.16 DEBUG component.func line=9,241,821 per_sec=22,142

I wanted to get the average of these per_second values, and so I wrote a little
filter to extract the number:

    head log -1 | perl -nE'/per_sec=(\S+)/ and say $1'
     22142

However that gave me output like "22,124", which wasn't yet ready for
averaging. So I spend a minute or two fiddling with the filter and ended up with
the follwing:

    cat log | perl -nE'/per_sec=(\S+)/ and do { ( $a =$1 ) =~ s/,//g; say $a}'

Not too bad, and with a bit more golfing I could have gotten it down to
something shorter. However, splitting it up would have made it even easier:

    head -1 log | perl -nE'/per_sec=(\S+)/ and say $1' | tr -d ','
     22142

The advantage of this approach is that I don't have to remember some special
perl syntax. I spent too much time messing around, trying to get it right when
it would have been simpler to refine it in two minimal filters that I could
write correctly the first time (or with 5 seconds looking at the tr manpage
after `tr ',' ""` didn't work.


To conclude this recipe, to compute the average, I just piped the resulting
values into the `stats` script, referenced below. Again, I could have written
some more perl to aggregate values and then print the results at eof or in an
end block, but I'd have spent a bit more time fiddling (or googling), and I
really just had a simple 60 second question to see if the average.

### collapse or replace spaces and newlines

perl has a few character classes in regular expressions that are worthwhile:

* \s is for general whitespace (spaces, newlines and tabs)
* \h is for horizontal whitespace (spaces and tabs)
* \v is for vertical whitespace (newlines)
* \t is for tabs

So, to collapse multiple spaces or tabs into a single character (":" in this case):

    printf "a b c\nfoo bar baz\n" | column -t | tee data
     a    b    c
     foo  bar  baz

To collapse the (horizontal) spaces and tabs:

    perl -pE's/\h+/:/g' data
     a:b:c
     foo:bar:baz

To collapse the vertical newlines:

    perl -pE's/\v+/:/g' data   # or \n
     a    b    c:foo  bar  baz:

To collapse both spaces and newlines:

    perl -pE's/\s+/:/g' data
     a:b:c:foo:bar:baz:

### convert spaces to newline with tr or perl

tr is a simple solution here, as long as you only want one to one replacement:

    echo "1 2 3" | tr " " '\n'
     1
     2
     3

As described  in the perl section above, you can use perl to replace spaces with newlines:

    echo "1   2 3" | perl -pe's/ +/\n/g' 
     1
     2
     3
 
### remove newlines with perl

Replace newlines, or vertical whitespace (a bit more cross-platform):

seq 10 | perl -pe's/\v/ /g' 
 1 2 3 4 5 6 7 8 9 10 

Keep the final newline:

seq 10 | perl -pe's/\v/ / unless eof'
1 2 3 4 5 6 7 8 9 10


### reshape text with rs

A little tool I discovered recently is `rs` :

- http://manpages.ubuntu.com/manpages/xenial/man1/rs.1.html
- https://github.com/chneukirchen/rs
- appears built-in on mac

    seq 12 | rs 3 4
     1   2   3   4
     5   6   7   8
     9   10  11  12

    seq 6 | rs 1 0
     1  2  3  4  5  6

And just to show it is smart about collapsing arrays:

    seq 6 | rs 2 3 | rs 1 0
     1  2  3  4  5  6

I'm just playing with this a bit, there are a lot more options, and it doesn't
appear to be widely available.

### merge sort  multiple files of sorted data

Sometimes I have data that has already been sorted by another process. GNU sort
is very powerful and has a variety of features like parallel sorting and large
file sorting (more on sort below). It also provides merge-sorting of pre-sorted
files via the `--merge` switch.

    sort --merge sorted1 sorted2 sorted3

### paste: add files side by side

```
seq 1 5 > a
seq -w 0 .5 2 > b
seq 6 10 > c

paste a b c
 1    0.0    6
 2    0.5    7
 3    1.0    8
 4    1.5    9
 5    2.0    10
```

Note that you can also use paste to transform a single stream into multiple
columns by including the desired number of stdin reads, `paste - -` or
paste `- - - - -`:

seq 10 | paste - - -
 1	2	3
 4	5	6
 7	8	9
 10		

### join: intersect two files

`join` is use to match rows or items in one file with another.

It can be used, much like a database, to join rows that match other
rows based on a field from each file. It requires each file to be
sorted on the join field, however.

Other than basic lookup, I also use join to fill in missing values in a
sequence. For example, I have a file with per-minute error counts, and I want
to see both the minutes with errors, and the minutes without errors (which are
not present in the input). The errors data could be the output of a frequency
count pipeline, described below.

    cat > errors <<EOM
    12	12:31
    12	12:34
    19	12:32
    23	12:36
    99	12.37
    EOM

And we'll generate all the minutes in our range. See the generation section or
the section on gnu parallel for some additional ideas, but here's an example of
using the seq command with a template. tee prints the ouput both to a file, and
to the screen.

    seq -f "12:%02.0f" 31 37 | tee minutes
    12:31
    12:32
    12:33
    12:34
    12:35
    12:36
    12:37

`join` requires that the both input files are pre-sorted by the join key, and so
we will have to re-sort the errors table before joining. I'll use sort and sort
"inplace", overwriting the original file: However, a temp file would work just
as well. I'm sorting on field #2, and sort uses whitespace as column delimiters
by default. We'll skip the items table, since it's already sorted.

    sort -o errors -k 2 errors

Now we're ready to do the join. We need to specify what fields we want to join
on from each file. Since we want the first (and only) field from minutes, we can 
omit it. `-a 2` tells join to show missing matches from the minutes file, 
and `-1 2` tells join to use the join key from file 1, field 2.

    join  -a 2 -1 2 00 errors minutes
     12:31 12
     12:32 19
     12:33
     12:34 12
     12:35
     12:36 23
     12:37 99

With an additional filter, we could add a default value of zero, but it is
now clear in context which values are missing.

### Concatenate files, skipping header line

Often I want to combine multiple files that already have headers, most commonly
with CSV data. However, sometime I have data with a comment block at the top.

the `csvstack` command (`pip install csvkit`) is ideal if the data is csv.

    csvstack f1.csv f2.csv f3.csv

Here's a simple script to join files with headers:

    #!/usr/bin/env python
    """join files with a header line"""

    from __future__ import print_function
    import fileinput

    for line in fileinput.input():
      if not fileinput.isfirstline() or fileinput.lineno() == 1:
        print(line, end="")

### Remove the first n lines of a file with tail

Tail is typically used to display the last n lines of a file, e.g. get the bottom top values with `sort data | tail -5`

However, it can also skip lines if you provide a positive offset, e.g. `tail +10`
The catch is that the number you provide is where it will start printing, not how many
lines will be skipped.

    # starts on line 3
    seq 5 | tail +3 
    3
    4
    5

Note: If you actually want the top 5 values from a dataset, it's more common to
reverse the sort and take the first values, e.g. `sort -nr data | head -5`
which should be just as fast to sort, and avoids reading through the entire
file just to get the last few values.

### Sort a file with a header

Sometimes you have a file that has a multiline header, and you'd like to sort
the data but keep the header. One nice technique is to print the header to
stderr, and then process the rest of the file before displaying it. This is
also a nice way to provide "users" with a variety of options to sort the
output, assuming it is in easily sortable form. 

It's pretty easy to do this with head and tail, although you have to remember
that the offsets are off by one:

    cat > data <EOM
     # Here's some data
     # with a header
     20
     5
     1
     15
     EOM

Now, I'd like to sort the data in descending order, but the header gets sorted
as well.

    sort -nr data
     20
     13
     5
     1
     # with a header
     # Here's some data

Instead, if we put the header on stderr, and then sort the rest, we'll get what we want

    head -2 data > /dev/stderr; tail +3 data  | sort -nr
     # Here's some data
     # with a header
     20
     13
     5
     1

Now, with this small behead script, we can sort only the data portion
of a file:

    #!/usr/bin/env perl
    use Getopt::Std;
    my $opt_n = 1;
    getopts('n:');

    while(<>) {
      if ($. <= $opt_n ) {
        print STDERR;
      } else { 
        print
      }
    }


    behead -2 data | sort -nr
     # Here's some data
     # with a header
     20
     15
     5
     1

Another interesting use of behead is to quickly see both the first and last value of some input,
like a range query. 

IMPORTANT NOTE: behead prints output to stderr, so this isn't suitable for piping to another
command, but can be useful just to see in the terminal.

    seq -w 1 10 | behead | tail -1
     01
     10

### put data into a specific number of columns with pr

The pr command is used to format text files for printing, and it has a large
set of options. It can also be used to do some useful things for display.

Note that the -t option is required to skip the unwanted page header that is
intended for print output.

Three columns. Fill down columns first.

```
seq 10 | pr -t -3
1            5            9
2            6            10
3            7
4            8
```

Three columns. Fill across rows first.

```
seq 10 | pr -t -3 -a
1            2            3
4            5            6
7            8            9
10
```

### making data tables with column

Sometime you have unevenly spaced fields (or words), and you'd like to turn it
into nice white-space separated columns. The column command has a table mode
for just this. I often use this to either pretty print a command's fields, or
for pretty printing parts of a log file (note that it's not good for the entire
line, as it works best when there are a limited (and constant) number of
columns.
 
    cat > mytxt <<EOF
    the quick brown fox
    jumped over the lazy
    dogs and it was
    so very, very funny
    EOF

Use the table mode `-t` to turn it into variable width columns, each sized
according to the largest item.

    column -t mytxt
     the     quick  brown  fox
     jumped  over   the    lazy
     dogs    and    it     was
     so      very,  very   funny

### Use column to create a flexible number of columns to fill the width.

pr is useful when you know how many columns you want to create. `column` also
has a mode to create columns, but unlike pr, you set the width you want, and
column will create an appropriate number of columns to fill it.


Fill down columns first.

```
seq 30 | column -c 40
1       7       13      19      25
2       8       14      20      26
3       9       15      21      27
4       10      16      22      28
5       11      17      23      29
6       12      18      24      30
```

Same as above, but fill across first.

```
seq 30 | column -c 40 -x
1       2       3       4       5
6       7       8       9       10
11      12      13      14      15
16      17      18      19      20
21      22      23      24      25
26      27      28      29      30
```

### joining all lines with xargs

If you just want all the items on the same line, `xargs` is quick and dirty,
joining with spaces. `xargs echo` can also be used.

    seq 20 | xargs
     1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

Use a perl transformation like `perl -pe's/\n/:/ unless eof'` to join with other characters.

To have a specific number of columns, still space separated, have xargs break
it up for you. here's we're chosing 5 at a time, and notice that the alignment
isn't very good. See `column` below for how to align columns.

    seq 20 | xargs -n5 echo
     1 2 3 4 5
     6 7 8 9 10
     11 12 13 14 15
     16 17 18 19 20

See below for the section on xargs. 

## Grouping data

### Find distinct items, removing duplicates

    cat data | sort -u

    cat data | sort | uniq

### Find unique items

    cat data | sort | uniq -u

### Find duplicate items

    cat data | sort | uniq -d

### Find lines that are in one file, but not in another

Sometimes I have a list of all files, and then a list of files that I want to keep, and I need to subtract the keepers aand work on the rest.

If both files are sorted (or can be sorted), then you can use either the `comm` utility, or `diff`.

comm takes two files, and reports of files that are in a, b or both.

So, to file files that are in `all`, but not in 'keep', tell comm to suppress the lines in the second file (-2), and in both files (-3):

    comm -23 all keep

You can also grep the output of diff, which is most useful if you want to get a
bit of context around missing lines. Lines removed from the first file are
prefixed with a ' <', or '-' in unified (-u) mode. You'll need to do a little
post-processing on the output to remove the diff characters, so `comm` is often
an easier choice.

    diff -u all keep | egrep '^-' 

If it's not practical to sort the files, then you may need to do a little
actual coding to put the lines from one file into a dictionary or set, and
remove the lines from the other.


### Split data into files based on a field

awk has a really simple way to split data into separate files based on a field. 

`{print > $1}`, which prints the line into a file named in the first column.

Here's a more concrete example, using this techinque in conjuction with a program called `average` that, not surprisingly, computes the average of its inputs. The input is a request rate, and the date portion of a timestamp extracted from a log file:

The input date:

    10:50:41 $ head -5 /tmp/a
     2017-11-22	17918
     2017-11-22	22122
     2017-11-22	23859
     2017-11-22	24926
     2017-11-22	25590

Put each rate into a file named for the day:

    10:51:12 $ awk '{ print $2>$1}' /tmp/a

Verify the files:

    10:51:30 $ ls
     2017-11-22  2017-11-23  2017-11-24  2017-11-25  2017-11-26  2017-11-27

Finally, compute an average based on a special purpose program (or your own
oneliner)

    10:51:39 $ for f in 2017*;do  echo -n "$f "; average $f; done;
     2017-11-22 28623.5339943343
     2017-11-23 32164.1470966969
     2017-11-24 41606.0775438271
     2017-11-25 44660.3379886831
     2017-11-26 43758.5492501466
     2017-11-27 43080.1879794521

Naturally, there are other ways to do this specific computation, 
e.g. `cat /tmp/a | datamash --group 1 mean 2`, 
but sometimes it's useful to split the files for later processing.

See http://www.theunixschool.com/2012/06/awk-10-examples-to-split-file-into.html for some more examples.


## Frequency counts and distributions

### get a frequency count of items, or find common items

    # pipe into head or tail to get the most or least frequent items
    cat data | sort | uniq -c | sort -nr 

### Find the n most common items

    # find tps 7 most common items
    cat data | sort | uniq -c | sort -nr  | head -7

### Better frequency counts

https://github.com/wizzat/distribution

Lets take some random words, repeat each one a random number of times, and then
see what the frequency distribution of the most common words look like:

    cat randwords | perl -ne'$a=$_; print $a for 0..int(rand(25))' | distribution.py
               Key|Ct (Pct)   Histogram
       accelerator|25 (6.05%) ------------------------------------------------------
          absterge|25 (6.05%) ------------------------------------------------------
       Acanthodini|25 (6.05%) ------------------------------------------------------
           Abramis|25 (6.05%) ------------------------------------------------------
       acclimation|24 (5.81%) ---------------------------------------------------
         acatharsy|24 (5.81%) ---------------------------------------------------
      accelerative|23 (5.57%) -------------------------------------------------
    acanthopterous|23 (5.57%) -------------------------------------------------
           Abraham|22 (5.33%) -----------------------------------------------
            Abipon|21 (5.08%) ---------------------------------------------
       accentuable|18 (4.36%) ---------------------------------------
    Acanthocephala|18 (4.36%) ---------------------------------------
            abduce|17 (4.12%) -------------------------------------
              Abba|17 (4.12%) -------------------------------------
            absume|14 (3.39%) ------------------------------    

### Histogram of values

https://github.com/bitly/data_hacks

    pip install data_hacks

Generate 1000 random values from 0-300 and generate a histogram:

    perl -E'say rand(300) for 1..1000' | histogram.py
    # NumSamples = 1000; Min = 0.12; Max = 299.94
    # Mean = 148.416700; Variance = 7602.103173; SD = 87.190041; Median 151.018961
    # each ∎ represents a count of 1
        0.1198 -    30.1021 [   115]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       30.1021 -    60.0845 [    94]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       60.0845 -    90.0668 [   104]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       90.0668 -   120.0491 [    98]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      120.0491 -   150.0315 [    84]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      150.0315 -   180.0138 [    92]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      180.0138 -   209.9962 [   109]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      209.9962 -   239.9785 [   118]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      239.9785 -   269.9608 [   103]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      269.9608 -   299.9432 [    83]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎

Note: I removed some of the bucket indicators to make the lines shorter.

## SPECIALIZED TOOLS FOR AGGREGATION, SUMMARY, ANALYSIS AND REPORTING

I use a wide variety of tools for aggregation ranging from relatively simple to
complex and fully featured. Once I have filtered and extracted the data I want,
I have a set of core tools I use for most summarization. Some are small,
single-file scripts that I just copy to a new machine if needed, while others
are full-blown packages.

Note that I won't really talk about actual databases, as the data import/export process usually ends up
being a significant factor (except for csv data via `csvquery`)

The ones that I tend to use most are:

### stats

`stats` is a compantion script to (scut)[https://github.com/hjmangalam/scut]
that prints discriptive statistics for a single column of numeric inputs. 

https://github.com/hjmangalam/scut/blob/master/stats

    seq 10 | stats
     Sum       55
     Number    10
     Mean      5.5
     Median    5.5
     Mode      FLAT  
     NModes    No # was represented more than once
     Min       1
     Max       10
     Range     9
     Variance  9.16666666666667
     Std_Dev   3.02765035409749
     SEM       0.957427107756338
     95% Conf  3.62344286879758 to 7.37655713120242
               (for a normal distribution - see skew)
     Skew      0
               (skew is 0 for a symmetric dist)
     Std_Skew  0
     Kurtosis  -1.40181818181818
                (K=3 for a normal dist)

### csvstat

`csvstat` is another part of the great `csvkit` toolbox. It prints descriptive
stats from csv files. You can also process a single numeric column without a
header by using the -H flag, although it's not particularly fast. Here's an example of using it to generate some stats on a single column, although it will do similar goodness for a csv file with multiple columns. Naturally, for non-numeric columns, there will not be as many 

    jot -r 1500 1 999 | csvstat -H
     /usr/local/lib/python2.7/site-packages/agate/table/from_csv.py:88: RuntimeWarning: Column names not specified. "('a',)" will be used as names.
       1. "a"
     
      Type of data:          Number
      Contains null values:  False
      Unique values:         764
      Smallest value:        1
      Largest value:         999
      Sum:                   746,595
      Mean:                  497.73
      Median:                494.5
      StDev:                 288.637
      Most common values:    370 (7x)
                             994 (7x)
                             770 (6x)
                             316 (5x)
                             488 (5x)
     
     Row count: 1500

Here's an example of getting stats on a simple 2-column csv file. Notice that
the error message has gone away because we added the headers.

    (seq 10; jot -r -c 10 97 120 ) | column -c 20 | csvformat -t | ( echo "num,letter"; cat;) | tee sample.csv
     num,letter
      1,g
      2,k
      3,a
      4,p
      5,m
      6,q
      7,l
      8,w
      9,r
      10,d

Now, generate stats on all of the columns:

    csvstat sample.csv
        1. "num"
      
       Type of data:          Number
       Contains null values:  False
       Unique values:         10
       Smallest value:        1
       Largest value:         10
       Sum:                   55
       Mean:                  5.5
       Median:                5.5
       StDev:                 3.028
       Most common values:    1 (1x)
                              2 (1x)
                              3 (1x)
                              4 (1x)
                              5 (1x)
      
        2. "letter"
      
       Type of data:          Text
       Contains null values:  False
       Unique values:         10
       Longest value:         1 characters
       Most common values:    a (1x)
                              c (1x)
                              f (1x)
                              h (1x)
                              k (1x)
     Row count: 10 

### datamash

do computation and stats on the command line

#### quick grouped stats with datamash

For very simple summary stats, I often turn to the `stats` command or
`csvstat`. However, if I want to do a bit more, like aggregate by one or more
columns, `gnu datamash` is very useful. It handles large streamed data sets
very quickly, and has a variety of statistical functions available. By default
it breaks on continuous whitespace. Use the -t option to break on tabs,
possibly after transforming data via `csvformat -T` if you have csv input data.

From the [datamash manual](https://www.gnu.org/software/datamash/manual/datamash.html):

```
cat > scores.txt << EOF
Name        Subject          Score
Bryan       Arts             68
Isaiah      Arts             80
Gabriel     Health-Medicine  100
Tysza       Business         92
Zackery     Engineering      54
EOF
```
datamash --sort --headers --group 2 mean 3 sstdev 3 < scores.txt

```
GroupBy(Subject)   mean(Score)   sstdev(Score)
Arts               68.9474       10.4215
Business           87.3636       5.18214
Engineering        66.5385       19.8814
Health-Medicine    90.6154       9.22441
Life-Sciences      55.3333       20.606
Social-Sciences    60.2667       17.2273
```

#### Cross tables/pivot tables with datamash

    cat <<EOF | csvformat -T > data2.tsv
    year,state,name,amount
    2017,CA,"Foo, Bar",100
    2017,CA,"Boo, Baz",200
    2016,NJ,"Hoo, Dat",75
    2016,CO,"Why, Not",33
    EOF

Create a pivot table that has the year column vs. the state column, summing
amount column for each cell.

    cat data2.tsv | datamash -H crosstab 1,2 sum 4
     GroupBy(year)   GroupBy(state)  sum(amount)
             CA  CO  NJ
     2016    N/A 33  75
     2017    300 N/A N/A




## csv/tsv:

### csvkit

csvkit is an excellent set of tools (and python libraries) for working with CSV data. I work with a variety of csv data,
and I use many of these frequently.

I tend to use:

* csvlook - pretty printing of csv files
* csvcut - extract columns from CSV
* csvsql - run SQL queries against CSV data
* csvstats - summary statistics for CSV file


Here's an introduction:

https://source.opennews.org/articles/eleven-awesome-things-you-can-do-csvkit/

## json

- jq - CLI query language for json. Doesn't handle very large ints.
- jsonpp, json_pp - pretty printing, 
- `python -m json.tool` - pretty printing. Doesn't handle json per lin

### jq

Here's some sample json (created using the jo json authoring tool)

    { jo user[name]=jud user[id]=17 ; jo user[name]=joe user[id]=22;} | tee json1
    {"user":{"name":"jud","id":17}}
    {"user":{"name":"joe","id":22}}

jq has a fully-featured query language, but since I don't use the more advanced features very often,
I just remember how to index down into object, and print out the raw values:

    # pretty print with colorization
    jq . myfile.json

    # extract user.name from every object
    jq .user.name myfile.json
    "jud"
    "joe"

    # get the raw (unquoted) values.
    jq -r .user.name json1
    jud
    joe

I nearly always use jq for my json needs. However, I've recently been dealing with json that contains very large numeric ids.
Unfortuntely jq rounds large integers.


    echo '{"a":11111222223333344444}' | jq .
    {
      "a": 11111222223333345000
    }

    echo '{"a":11111222223333344444}' | python -m json.tool
    {
        "a": 11111222223333344444
    }

So I have been using other tools to pretty print json, like jsonpp and/or json_pp.

The python json.tool pretty printer handles big ints, but doesn't handle newline delimited json. I just saw the newlinejson package, which could help.
Here's a simple python solution:


    #!/usr/bin/env python
    from __future__ import print_function
    import fileinput
    import json
    for line in fileinput.input():
        print(json.dumps(json.loads(line.rstrip('\r\n')), indent=2))


## Generating data

### Generating columns of data by column

    seq 20 | pr -t -3 | column -t
    1  8   15
    2  9   16
    3  10  17
    4  11  18
    5  12  19
    6  13  20
    7  14

### Generating columns of data by row

    seq 20 | pr -t -3 -a | column -t
    1   2   3
    4   5   6
    7   8   9
    10  11  12
    13  14  15
    16  17  18
    19  20

### Generating a sequence of letters:

    perl -E'say for "a".."d"'
     a
     b
     c
     d

### Generating random numbers

10 random numbers between 0 and 19

    perl -E'say int(rand(20)) for 1..10'

#### jot

Generate various sequences and random numbers

10 ints between 0 and 100

    jot -r 10 0 100

5 floats between 0.000 and 1.000

    jot -r 5 0.000 1.000

random letters

    jot -r -c 10 97 122


### Generating permutations with shuf

`shuf`, part of `coreutils`, is useful for generating random permutations.

shuf is best known for generating a "shuffled" version of a file, or selecting
random lines. However, it can also be used to generate some sample data quickly
given a few input values. The `-r` flags allows repeats. `-n 100` selects 100
samples. `-e` treats additional command line parameters like input lines.

In this example, I want to take 100 random selections 'foo', 'bar' or 'baz'

    shuf -r -n 100 -e foo bar baz | head
     baz
     baz
     baz
     baz
     bar
     foo
     foo
     bar
     bar
     baz

Here's a more complicated example of generating some test scores for some
random student ids in random classes:


    seq 100 | gshuf -n 100 -r > student_ids.txt
    gshuf -n 100 -r -e math science art > classes.txt
    seq 50 100 | gshuf -n 100 -r > scores.txt
    (
      echo "id class score";
      paste -d " " student_ids.txt classes.txt scores.txt;
    ) > report.tsv

Now, with these scores, let's get some aggregate data

    cat report.tsv | datamash -sH --wh --group 2 mean 3 | column -t
     GroupBy(class)  mean(score)
     art             73.214285714286
     math            73.461538461538
     science         72.21875
 
## Sorting

### gnusort on osx via coreutils

On osx, you will probably want gnusort, which can be installed via `brew install coreutils`

#### sort items lexicographically, numerically (gnu sort)

    sort
    sort -n

#### sort with size units, (k, m, etc)

gnu sort can sort human units, like 10K, 100g.

    du -h | gsort -h -r | head -5
    256K    .
    212K    ./.git
     92K    ./.git/objects
     44K    ./.git/hooks
     20K    ./.git/logs


## Batch and parallel execution with xargs and parallel

There are a few commands that are generally useful when working with many files.

### xargs 

xargs allows you to generate commands by piping in parameters. 

A trivial example is to compress the 3 oldest files in the directory. I list
the csv files, sorted by age(recent first), and then take the last 3. These 3
files, one per line, are passed into xargs, which sends them to whatever
command I specify as arguments.

    ls -1 -t *.csv | tail -3 | xargs -t gzip
     gzip 19.csv 18.csv 17.csv

I use a few options frequently:

*  `-n 1` to only pass one argument at a time, like a for loop. Note that many
   of the common uses of xargs can also be replaced by a simple bash for loop.
* parameter subsitution with `-I %`. If I want multiple replacements, or need to an an extension, that's a good way.

    ls -1 *.sql | xargs -n 1 -I % echo mycommand --logfile %.log %
     mycommand --logfile 201701.csv.log 201701.csv
     mycommand --logfile 201702.csv.log 201702.csv

* parallel execution of commands.

```
# gzip csv files, with four parallel processes.
# print lines as we execut them, and send one file
# at a time to each invocation

ls -t -1 *.csv | xargs -P 4 -t -n 1 gzip   
 gzip 04.csv
 gzip 03.csv
 gzip 02.csv
 gzip 01.csv
```

Which leads into the next section, for a higher-powered alternative.

### GNU parallel

Parallel is a powerful and huge tool, and has many pages of manuals and examples.

However, there are a few key things that I like about running commands via parallel:

* easily create separate log files for each invocation.
* run commands on multiple machines

See also: [sem](https://www.gnu.org/software/parallel/sem.html), part of the
gnu parallel package, which allows you to easily limit the number of concurrent
proceses without the complexity of parallel. Very useful for running N jobs in
parallel inside a simple for loop.

## Misc

### Progress bars in pipes

Sometimes I am sending a lot of data through a pipeline, and I'd like to have
an idea of how quickly it is proceeding, or if it's still going at all.

There's a useful command that I discovered for this called pv. `brew install pv` or `apt-get install pv`

    seq 50111222 | pv -lapbet | wc -l
     23.1M 0:00:07 [3.29M/s] [                  <=>

pv can produce a litle curses progress meter that updates as you go. It has a lot of formatting options,
including the lines format, the default bytes format, ETA and other goodies.

You can also create a trivial monitor in perl:

    # print the line number ever 1MM lines
    perl -pE'say STDERR $. if $. % 1_000_000 == 0'


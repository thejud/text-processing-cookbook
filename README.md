# text-processing-cookbook

A cookbook of tools and techniques for processing text and data at the linux command line

I often find myelf processing text on the linux command line, logfiles, data files,
command output, etc... Using these operations follow the following pattern:

Many of my data processing tasks follow this pattern:

* FILTER the input, selecting a set of lines that I want
* TRANFORM the selected lines into a more useful format
* REFILTER or JOIN the transformed data
* AGGREGATE the data
* DISPLAY the aggregate data in an informative way

Due to the power and flexibility of linux pipes, I can quickly assemble a set
of commands that are very effective on small to medium sized datasets (able to
fit on a single machine). Without doing a lot of programming, I can do
exploratory analysis, and answer many types of questions quickly.


This document describes a variety of linux tools (built-in and/or open source)
that I've found useful for various parts of the progress.

Conventions: In code blocks, the command is left justified, while output from
the command is indented by one space. I find it annoying to remove the "$ "
prefix from commands when copying and pasting them, so you should be good to
go. I also use the `cat foo | bar` form rather than `bar < foo` because I've
fat-fingered '>' instead of '<' one too many times, overwriting my input file.
Also, I also use most of these scripts as part of a larger pipeline. Here's an
example of how a command and its output will be formatted.

    seq 10 | head -3
     1
     2
     3
 
## Extracting data

Extraction is a subset of transformation, but it is important enough to have its own
section.

perl, sed and awk are all common tools for both selection and extraction

### Extracting one or more columns with awk

    # breaks on any whitespace
    cat data | awk '{print $3}'

### extracting fields with cut

Cut is quite strict, but useful when you have fixed delimiters, or want to extract things by character position

### Extract by character position

    cat > alpha <<EOF
     abcdef
     gehijk
     EOF

    cat alpha | cut -c '2-4,6'
     bcdf
     ehik

### Extract by field widths with awk (and in2csv)

Sometimes you will have fields of known (but possibly variable) width, AKA
fixed width format.

awk can be used to extract the fields (you may need to install gnu awk)

    echo aaaaBBcccccDe | awk '$1=$1' FIELDWIDTHS='4 2 5 1 1' OFS=, 
    aaaa,BB,ccccc,D,e

from https://stackoverflow.com/a/28562381

Note that you can also use `in2csv` (part of `csvkit`) to convert fixed with
to csv files with headers. It requires a schema file, so this is probably most
practical if you find yourself doing this frequently for the same schema, or
there are a LOT of fields and you probably need to iterate through them anyway.


### Convert whitespace-delimited columns to csv

This can be relatively simple. If you know that you data doesn't contain
any additional commas, you can do a simple substition:

    perl -pe's/\h+/,/g';  # horizontal space, no newline
    perl -anE'say join(",", @F)'

If you can't be sure that there won't be commas in the
fields, you'll want to do proper quoting. Use a real
csv tool.

    perl -anE'say join("\t", @F)' | csvformat -t -h

### Extract by position with simple delimter

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

### cutting columns, other tools

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

### for CSV data, use csvcut

`csvcut` is part of the `csvkit` suite

## Transformation tools

There's not a really clear line between extraction and transformation.

perl is my tool of choice for many line-oriented transformations. It's worth learning a few tricks,
and invensting some time in either perl, sed or awk.


### General transformation with perl -pE and -nE

The perl -p option turns on filter mode. Any changes made by the expression
argument (-e or -E) will be applied, and then each line will be printed. Using
regular expressions is a good way to remove parts of the line, or add to it.

Here's an example of removing the subsecond timestamp from a log line:

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -pe's/\.(\d*) / /'  
     2017-11-01T12:14:22 ERROR critical

You can also extract portions of the line by matching against the entire line. Here's
a moderately complicated regular expression that extracts the hour:minute pair, and the log level (ERROR or FATAL). This
might be the first step in analyzing errors per minute.

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

Also, like anything other part of your pipelin, it's fine to clean up your
output in multiple smaller, simpler filters. I often do this because it's
easier to apply fixes than to get one large regex just right. Naturally, if
you're building a high-volume or production pipeline, it's probably worthwhile
to take the time to get it right. 

Note that I'm using tee /dev/stderr to give some diagnostic output at each
stage in the pipeline so you can see how the line is progressively refined. You
would only want to do that for debugging or development. Although see the `pv`
recipe later for more on getting a progress meter for your pipeline.

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
    | perl -pe's/:\d\d / /' \
     2017-11-01T12:14:22.12352 ERROR
     12:14:22.12352 ERROR
     12:14:22 ERROR
     12:14 ERROR

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

#### Use column to create a flexible number of columns to fill the width.

column is specially designed to "columnate lists", with far fewer options that pr.

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

### joining all lines with xargs echo 

If you just want all the items on the same line, `xargs echo` is quick and dirty, joining
with spaces.

    seq 20 | xargs echo
     1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

Use a perl transformation like `perl -pe's/\n/:/g'` to join on other characters.

To have a specific number of columns, still space separated, have xargs break
it up for you. here's we're chosing 5 at a time, and notice that the alignment
isn't very good. See `column` below for how to align columns.

    seq 20 | xargs -n5 echo
     1 2 3 4 5
     6 7 8 9 10
     11 12 13 14 15
     16 17 18 19 20

See below for the section on xargs. 

### making data tables with column

Sometime you have unevenly spaced fields (or words), and you'd like to turn it
into nice white-space separated columns. The column command has also table mode
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

Use the table mode to turn it into variable width columns, each sized according
to the largest item.

    column -t mytxt
     the     quick  brown  fox
     jumped  over   the    lazy
     dogs    and    it     was
     so      very,  very   funny

## Grouping data

### Find distinct items, removing duplicates:

    cat data | sort -u

    cat data | sort | uniq

### Find unique items

    cat data | sort | uniq -u

### Find duplicate items

    cat data | sort | uniq -d

### get a frequency count of items, or find common items

    # pipe into head or tail to get the most or least frequent items
    cat data | sort | uniq -c | sort -nr 

### Find the n most common items

    # find tps 7 most common items
    cat data | sort | uniq -c | sort -nr  | head -7

### Better frequency counts

https://github.com/wizzat/distribution

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


## csv/tsv:

  - csvkit

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
I just remember how to index down into object:

    # extract user.name from every object
    jq .user.name json1
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


## Filter and select

grep is the linux go-to search tool, supporting fast searching using patterns
and regular expression.

I'll cover some other options here.

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

## Misc


### stats 

generate stats from numeric input

https://github.com/hjmangalam/scut

### datamash

do computation and stats on the command line


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

    # gzip csv files, with four parallel processes.
    # print lines as we execut them, and send one file
    # at a time to each invocation

    ls -t -1 *.csv | xargs -P 4 -t -n 1 gzip   
     gzip 04.csv
     gzip 03.csv
     gzip 02.csv
     gzip 01.csv

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


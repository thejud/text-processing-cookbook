# Transformation

perl is my tool of choice for many line-oriented transformations. It's worth
learning a few tricks, and investing some time with one or more of perl, sed or awk.

## General transformation with perl -pE and -nE

The perl -p option turns on filter mode. Any changes made by the expression
argument (-e or -E) will be applied, and then each line will be printed. Using
regular expressions is a good way to remove parts of the line, or add to it.

If you don't know anything about regular expressions, this will all seem very
mysterious, but if you do much text (or log) munging, it's worthwhile to learn
the basics. 

Here's an example of removing the date prefix of a timestamp from a log file,
which I have done when I want to compare activity at various times across several days.
My expression is a substitution: s/XXX/YYY/ and I'm replacing everything up to the first T
with the empty string:

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -pe's/^.*?T//'  
     12:14:22.12352 ERROR critical

You can also extract portions of the line by matching against the entire line.
Here's a moderately complicated regular expression that extracts the
hour:minute pair, and the log level (ERROR or FATAL). This might be the first
step in analyzing errors per minute.

    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -pe's/^.*?T(\d\d:\d\d):\S+ (ERROR|FATAL) .*$/$1 $2/'
     12:14 ERROR

I tend to prefer to only take the parts I want, rather than replacing the
entire line. perl's `-n` flag loops over all the input, but doesn't print
anything. The -E flag is an updated version of the -e flag that just makes some
of the more modern perl features available. I use `-E` mostly so that I can use
`say $var` instead of `print "$var\n"`, because say is shorter and automically
adds a trailing newline.


    printf "2017-11-01T12:14:22.12352 ERROR critical" \
    | perl -nE'/T(\d\d:\d\d):\S+ (ERROR|FATAL)/ and say "$1 $2"'
     12:14 ERROR

## Create several simple filters rather than one complicated one

Like any other part of your pipeline, it's fine to clean up your
output progressively with multiple smaller, simpler filters. I often do this
because it's easier to apply fixes than to get one large regex just right.
Naturally, if you're building a high-volume or production pipeline, it's
probably worthwhile to take the time to get it right in fewer steps. 

Here's the filter from the previous recipe broken down into several steps.

Note that in this example I'm using `tee /dev/stderr` to give some diagnostic
output at each stage in the pipeline so you can see how the line is
progressively refined. You would only want to do that for debugging or
development. The output appears at the end, and I've added some blank lines `\`
just to visually separate the steps.

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
time looking up the particular syntax for a more complicated regular expression.

Recently, I've been dealing with billions of records in blocks of 10 million or
so. In the logfiles for these tools, I use numbers with comma separation so
it's a little easier to quickly see the exact magnitude of the numbers. However,
the comma format isn't as easy for doing math.

Here's a partial log line. I typically use key=value format in my log as well,
as it is both clear and easy to parse.

    2017-11-20T15:33.16 DEBUG component.func line=9,241,821 per_sec=22,142

I wanted to get the average of these per_second values, and so I wrote a little
filter to extract the number:

    head log -1 | perl -nE'/per_sec=(\S+)/ and say $1'
     22,142

However that gave me output like "22,124", which wasn't yet ready for
averaging. So I spent a minute or two fiddling with the filter and ended up with
the follwing:

    cat log | perl -nE'/per_sec=(\S+)/ and do { ( $a =$1 ) =~ s/,//g; say $a}'

Not too bad, and with a bit more golfing I could have gotten it down to
something shorter. However, splitting this procedure up into two separate
transformations would have made it much easier:

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
END block, but I'd have spent a bit more time fiddling (or googling), and I
really just had a simple 60 second question to see if the average was above
or below the last few values I saw in the logfile.

## collapse or replace spaces and newlines

perl has a few character classes in regular expressions that are worthwhile:

* \s is for general whitespace (spaces, newlines and tabs)
* \h is for horizontal whitespace (spaces and tabs, NOT newlines)
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

## convert spaces to newline with tr or perl

tr is a simple solution here, as long as you only want one to one replacement:

    echo "1 2 3" | tr " " '\n'
     1
     2
     3

Collapse multiple spaces with the squeeze (-s) option:

    echo "1   2 3" | tr -s " " '\n'
     1
     2
     3

As described in the perl section above, you can use perl to replace spaces with newlines:

    echo "1   2 3" | perl -pe's/ +/\n/g' 
     1
     2
     3

Or via autosplit + join:

    echo "1   2 3" | perl -anE'say join "\n", @F'
 
## remove newlines with perl

Replace newlines, or vertical whitespace (a bit more cross-platform):

    seq 10 | perl -pe's/\v/ /g' 
     1 2 3 4 5 6 7 8 9 10 

Keep the final newline:

    seq 10 | perl -pe's/\v/ / unless eof'
     1 2 3 4 5 6 7 8 9 10


## reshape text with rs

A little tool I discovered recently is `rs` :

- http://manpages.ubuntu.com/manpages/xenial/man1/rs.1.html
- https://github.com/chneukirchen/rs
- appears built-in on mac


    seq 12 | rs 3 4
     1   2   3   4
     5   6   7   8
     9   10  11  12

or to transpose row and column order with `-t`:

    seq 11 | rs -t 3 4
     1   4   7   10
     2   5   8   11
     3   6   9

Or to collapse. Use 0 to automatically determine the other value:

    seq 6 | rs 1 0
     1  2  3  4  5  6

And just to show it is smart about collapsing arrays:

    seq 6 | rs 2 3 | rs 1 0
     1  2  3  4  5  6

    seq 6 | rs 2 3 | rs 0 5
     1  2  3  4  5
     6  

I'm just playing with `rs` a bit, there are a lot more options, and it doesn't
appear to be widely available. However, it's nice if you want to specify the
columns and rows.

## merge sort  multiple files of sorted data

Sometimes I have data that has already been sorted by another process. GNU sort
is very powerful and has a variety of features like parallel sorting and large
file sorting (more on sort below). It also provides merge sorting of pre-sorted
files via the `--merge` switch.

    sort --merge sorted1 sorted2 sorted3

## paste: add files side by side

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
`paste - - - - -`:

    seq 10 | paste - - -
     1	2	3
     4	5	6
     7	8	9
     10		

## join: intersect two files

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
    99	12:37
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
we will have to re-sort the errors table before joining. I'll sort inplace, by
telling sort to output to a file (the input file) when complete. Note that unlike
a normal output redirect, sort is smart enough to only create/rename the output
file when the sort operation is complete. However, a temp file would work just
as well. I'm sorting on field #2, and sort uses whitespace as column delimiters
by default. We'll skip the items table, since it's already sorted.

    sort -o errors -k 2 errors

Now we're ready to do the join. We need to specify what fields we want to join
on from each file. Since we want the first (and only) field from minutes, we can 
omit it. `-a 2` tells join to show missing matches from the minutes file, 
and `-1 2` tells join to use the join key from file 1, field 2.

    join  -a 2 -1 2 errors minutes
     12:31 12
     12:32 19
     12:33
     12:34 12
     12:35
     12:36 23
     12:37 99

With an additional filter, we could add a default value of zero, but it is
now clear in context which values are missing.

See also: `comm`

## Concatenate files, skipping header line

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

## Remove the first n lines of a file with tail

Tail is typically used to display the last n lines of a file, e.g. get the final (largest) 5 values with `sort data | tail -5`

However, it can also skip lines if you provide a positive offset, e.g. 
`tail +10` or `tail -n +10` The catch is that the number you provide is where 
it will start printing, *one less* than the number of lines will be skipped.

    # starts on line 3
    seq 5 | tail +3 
    3
    4
    5

Note: If you actually want the top 5 values from a dataset, it's more common to
reverse the sort and take the first values, e.g. `sort -nr data | head -5`
which should be just as fast to sort, and avoids reading through the entire
file just to get the last few values, which is what tail must do when reading
from a pipe.

## Sort a file with a header

Sometimes you have a file that has a multiline header, and you'd like to sort
the data but keep the header. One nice technique is to print the header to
stderr, and then process the rest of the file before displaying it. This is
also a nice way to provide users with a variety of options to sort the
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
printed to the terminal. 

**NOTE** This will NOT put the header into the output pipeline. See the bottom of this
recipe for an alternative.

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

If you want to capture both the header and the sorted body, use the command-block/subshell technique:

    ( head -2 data; tail +3 data | sort -nr ) > data.sorted


## put data into a specific number of columns with pr

The pr command is used to format text files for printing, and it has a large
set of options. It can also be used to do some useful things for display.
Unlike `rs`, it is standard on nearly every linux system.

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

## making data tables with column

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

## Use column to create a flexible number of columns to fill the width.

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

## joining all lines with xargs or paste

If you just want all the items on the same line, `xargs` is quick and dirty,
joining with spaces. `xargs echo` can also be used.

    seq 20 | xargs
     1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

To have a specific number of columns, still space separated, have xargs break
it up for you. here's we're chosing 5 at a time, and notice that the alignment
isn't very good. See `column` above for how to align columns.

    seq 20 | xargs -n5 echo
     1 2 3 4 5
     6 7 8 9 10
     11 12 13 14 15
     16 17 18 19 20

See below for the section on xargs. 

paste also provides a way to join all lines, the `-s` option. By default, paste
joins using a tab, but you can change that with the `-d`  option.

    seq 5 | paste -s -
     1       2       3       4       5

And to create comma-separated lists, provide a delimiter with the `-d` flag:

    seq 5 | paste -s -d, -
     1,2,3,4,5

## joining/transforming all except the last line with perl

Here's another way to join a set of lines, but keep the last one intact. Useful if you want to create a comma-separated.

Use a perl transformation like `perl -pe's/\n/:/ unless eof'` to join with other characters.

   seq 5 | perl -pe's/\n/:/ unless eof'
    1:2:3:4:5

This recipe can be generalized to apply any transformation to all except the last line.


## Transform one column at a time

Sometimes I want to work on only one column of a multi-column file. A very
common case is transforming the timestamp of some data, or a time-based ID to a
timestamp. Other possible cases include doing some lookup, hashing, and data obfuscation.

If the transformation is quite simple, perl or awk can be used:

    cat <<EOF | tee data
    1  2018-04-01  foo
    2  2018-04-01  bar
    3  2018-04-02  baz
    4  2018-04-03  cat
    EOF

Here's an example of using two simple awk filters to increment column 1, and
uppercase column 3:

    cat data | awk '$1=$1+7' | awk '$3=toupper($3)'
     8 2018-04-01 FOO
     9 2018-04-01 BAR
     10 2018-04-02 BAZ
     11 2018-04-03 CAT

A relatively complicated way to do the same thing with perl's autosplit:

    perl -anE'$F[0]+= 7; $F[-1] = uc($F[-1]); say join(" ", @F)' data
     8 2018-04-01 FOO
     9 2018-04-01 BAR
     10 2018-04-02 BAZ
     11 2018-04-03 CAT

### Split, transform and recombine columns

However, sometimes the transformation is more complicated than I'd want to try
inline, or I have an existing tool or filter that will work on a column of
data. One technique is to split the input into separate files by column,
process each column separately, and then recombine the column files with the
`paste` command. Note that this most useful when the number of columns is
relatively small. Here I'm doing it with the same 3-column file.

Create one file per colum:

    awk '{print $1}' data > a.01
    awk '{print $2}' data > a.02
    awk '{print $3}' data > a.03

Transform a column. Here we use a tempfile and would overwrite the original
file only if the command succeeds:

    cat a.02 | tr -d 'a' > tmp
    mv tmp a.02

Verify that the files still have the same number of lines:

    wc -l a.0*
       4 a.01
       4 a.02
       4 a.03
      12 total

Recombine the columns using paste. Separate with a space to match the input
file format.

    paste -d " " a.01 a.02 a.03
     1 2018-04-01 foo
     2 2018-04-01 br
     3 2018-04-02 bz
     4 2018-04-03 ct

Note that there are some problems with this approach. The most significant is
that your transformation script must return a single line of output for every
line of input, or the columns will become misaligned. Also, you end up
re-reading the input file several times, which may be ok with a small number of
columns, or a small file. Naturally, column extraction could be scripted with a
for loop, or a dedicated, smarter tool, but then things begin to get
complicated. 

Loop to extract columns 1,2 and 3:

    for i in `seq 3`; do awk "{print \$$i}" data > a.$i ; done

Finally, awk and paste are best for simple, whitespace delimited files, but you
could use something like `csvcut` (from `csvkit`, described below) and `paste
-d,` to handle CSV files.

Update:

Here's a cool solution for many columns via stack overflow
(https://stackoverflow.com/a/41863438). It makes use of the GNU split command
to group every Nth line together into a separate file without multiple passes through the
input. WARNING: The built-in split on OSX **DOESN'T** have the required
functionality, so you'll need to install the GNU version. e.g. `brew install
coreutils`. Under that same stack overflow question is a pure-awk solution, but
it's also a bit complicated.

Create a sample file with 10 columns:

    seq 50 | xargs -n10 | tee data
     1 2 3 4 5 6 7 8 9 10
     11 12 13 14 15 16 17 18 19 20
     21 22 23 24 25 26 27 28 29 30
     31 32 33 34 35 36 37 38 39 40
     41 42 43 44 45 46 47 48 49 50
     
Create one file per column by first collapsing the input rows into one cell per
line. These lines are split into 10 files, with every line going round-robin into
a separate (per-column) file.
Then transform the 9th column, and paste the files back together:

    cat data | tr ' ' '\n' | gsplit -nr/10 -d - /tmp/transform.
    perl -ni -E'say $_*10'  /tmp/transform.08
    paste -d ' ' /tmp/transform.*
     1 2 3 4 5 6 7 8 90 10
     11 12 13 14 15 16 17 18 190 20
     21 22 23 24 25 26 27 28 290 30
     31 32 33 34 35 36 37 38 390 40
     41 42 43 44 45 46 47 48 490 50

The `gsplit` (or `split` on linux) command magic is as follows:

* extract every 10th line into its own file, round robin style `-nr/10`
* create numeric filename suffixes `-d` (default to 2 digits. Starts with 00) 
* read from STDIN `-`
* write ouput files with a prefix `/tmp/transform.`

Note that the split files start at 00, so we transformed the 9th column in
`/tmp/tranform.08`. We did another trivial transformation (multiply the value
by 10).


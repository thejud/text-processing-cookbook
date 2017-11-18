# text-processing-cookbook

A cookbook of tools and techniques for processing text and data at the linux command line


## text tools

### Sorting

#### sort items lexicographically, numerically (gnu sort)

    sort
    sort -n

#### combine multiple files of sorted data:

    sort --merge file1 file2 file3

### combine multiple files

#### paste: add files side by side

```
$ seq 1 5 > a
$ seq -w 0 .5 2 > b
$ seq 6 10 > c

$ paste a b c
1    0.0    6
2    0.5    7
3    1.0    8
4    1.5    9
5    2.0    10
```

#### Concatenate files, skipping headers

If you want to join several files, but only keep the headers from the first one,
there are a few ways to do it.

the csvstack command (csvkit) is ideal if the data is csv.

You can also combine files without headers

    #!/usr/bin/env python
    from __future__ import print_function
    import fileinput
    for line in fileinput.input():
      if not fileinput.isfirstline() or fileinput.lineno() == 1:
        print(line, end="")

### put a sequence of data into columns

Note that the -t option is required to skip the unwanted header.

Three columns. Fill across first.

```
$ seq 10 | pr -t -3
1            5            9
2            6            10
3            7
4            8
```

Three columns. Fill across first.

```
$ seq 10 | pr -t -3 -a
1            2            3
4            5            6
7            8            9
10
```

Specify the total width, with a flexible number of columns.
Fill down columns first.

```
$ seq 30 | column -c 40
1       7       13      19      25
2       8       14      20      26
3       9       15      21      27
4       10      16      22      28
5       11      17      23      29
6       12      18      24      30
```

Same as above, but fill across first.

```
$ seq 30 | column -c 40 -x
1       2       3       4       5
6       7       8       9       10
11      12      13      14      15
16      17      18      19      20
21      22      23      24      25
26      27      28      29      30
```


### making evenly spaced columns from data

Sometime you have unevenly spaced fields (or words), and you'd like to turn it into nice
white-space separated columns. The column command has a table mode.
 
```
$ cat > txt <<EOF
the quick brown fox
jumped over the lazy
dogs and it was
so very, very funny
EOF

$ column -t txt
the     quick  brown  fox
jumped  over   the    lazy
dogs    and    it     was
so      very,  very   funny
```

Fill the rows first


#### join: intersect two files


## Grouping data

#### Find distinct items, removing duplicates:

    cat data | sort -u

    cat data | sort | uniq

#### Find unique items

    cat data | sort | uniq -u

#### Find duplicate items

    cat data | sort | uniq -d

#### get a frequency count of items, or find common items


    # pipe into head or tail to get the most or least frequent items
    cat data | sort | uniq -c | sort -nr 

#### Find the n most common items

    # find tps 7 most common items
    cat data | sort | uniq -c | sort -nr  | head -7

#### Better frequency counts

https://github.com/wizzat/distribution

    $ cat randwords | perl -ne'$a=$_; print $a for 0..int(rand(25))' | distribution.py
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

#### Histogram of values

https://github.com/bitly/data_hacks

    pip install data_hacks


Generate 1000 random values from 0-300 and generate a histogram:

    $ perl -E'say rand(300) for 1..1000' | histogram.py
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

## Whitespace delimited data

### Extracting one or more columns with awk

    # breaks on any whitespace
    cat data | awk '{print $3}'

### extracting fields with cut

Cut is quite strict, but useful when you have fixed delimiters, or want to extract things by character position

#### Extract by character position

    $ cat > alpha <<EOF
    abcdef
    gehijk
    EOF
    

    $ cat alpha | cut -c '2-4,6'
    bcdf
    ehik

#### Extract by position with simple delimter

    cat > data <<EOF	
    foo:bar:baz
    fun:stuff:today
    EOF

    $ cat data | cut -d: -f 1,3
    foo:baz
    fun:today

Note that it apparently ignores order

    $ cat data | cut -d: -f 3,1
    foo:baz
    fun:today

### cutting columns, third party solutions

#### f - trivial field extractor

https://blog.plover.com/prog/runN.html

    # quickly extract one column
    cat data | f 3

#### scut - swiss army knife of column cutters

https://github.com/hjmangalam/scut

    # zero indexed, easy to get many columns
    cat data | scut -f '2 1'

## Searching

* grep
* grep -P

### ag - the silver searcher

Fast search with perl regexes

## Transforming data

### Filtering

*  sed
* perl -nE'/(\d)$/ and say $1'

#### duplicating input lines a random number of times

A little perl to duplicate each line from 1 to 3 times.

    $ head -5 /usr/share/dict/words | perl -nE'$a=$_; print $a for 0..int(rand(3))'
    A
    A
    A
    a
    aa
    aal
    aal
    aal
    aalii
    aalii
    aalii


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
    $ jq .user.name json1
    "jud"
    "joe"

    # get the raw (unquoted) values.
    $ jq -r .user.name json1
    jud
    joe

I nearly always use jq for my json needs. However, I've recently been dealing with json that contains very large numeric ids.
Unfortuntely jq rounds large integers.


    $ echo '{"a":11111222223333344444}' | jq .
    {
      "a": 11111222223333345000
    }

    $ echo '{"a":11111222223333344444}' | python -m json.tool
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

You can also do a trivial monitor in perl:

  perl -pE'say STDERR $. if $. % 1_000_000 == 0'

## Generating data

### Generating columns of data by column

    $ seq 20 | pr -t -3 | column -t
    1  8   15
    2  9   16
    3  10  17
    4  11  18
    5  12  19
    6  13  20
    7  14

### Generating columns of data by row

    $ seq 20 | pr -t -3 -a | column -t
    1   2   3
    4   5   6
    7   8   9
    10  11  12
    13  14  15
    16  17  18
    19  20


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




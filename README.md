# text-processing-cookbook
A cookbook of tools and techniques for processing text and data at the linux command line


## text tools

### Sorting

#### sort items lexicographically, numerically (gnu sort)

    sort
    sort -n

#### combine multiple files of sorted data:

    sort --merge file1 file2 file3

### combine two files:

#### paste: add side by side

		$ seq 1 5 > a
		$ seq -w 0 .5 2 > b
		$ seq 6 10 > c

		$ paste a b c
		1    0.0    6
		2    0.5    7
		3    1.0    8
		4    1.5    9
		5    2.0    10

### put a sequence of data into columns

Columns first. Three columns

		$ seq 10 | pr -t -3
		1            5            9
		2            6            10
		3            7
		4            8

Rows first. Three columns.

		$ seq 10 | pr -t -3 -a
		1            2            3
		4            5            6
		7            8            9
		10

### making evenly spaced columns from data
 
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

#### Better frequency counts:

https://github.com/wizzat/distribution

    cat data | distribution.py

#### Histogram of values

perl -nE 'say rand() for 1..100' | histogram.py


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

  - jq
  - jsonpp


## Misc


### stats 

generate stats from numeric input

https://github.com/hjmangalam/scut

### datamash

do computation and stats on the command line



# Generating Data

## Generating columns of data by column

    seq 20 | pr -t -3 | column -t
    1  8   15
    2  9   16
    3  10  17
    4  11  18
    5  12  19
    6  13  20
    7  14

## Generating columns of data by row

    seq 20 | pr -t -3 -a | column -t
    1   2   3
    4   5   6
    7   8   9
    10  11  12
    13  14  15
    16  17  18
    19  20

## Generating a sequence of letters:

    perl -E'say for "a".."d"'
     a
     b
     c
     d

## Generating random numbers

10 random numbers between 0 and 19

    perl -E'say int(rand(20)) for 1..10'

### jot

Generate various sequences and random numbers

10 ints between 0 and 100

    jot -r 10 0 100

5 floats between 0.000 and 1.000

    jot -r 5 0.000 1.000

random letters

    jot -r -c 10 97 122


## Generating permutations with shuf

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
random student ids in random classes (note that here I'm using gshuf. On Mac
OSX, when installing coreutils via brew, it uses the 'g' prefix for the gnu
tools so they don't conflict with the osx standard (BSD) utilities of the same
name). Here I'm also using (...) to combine the output of multiple commands,
and converting spaces to tabs during output so I have an actual TSV file:


    seq 100 | gshuf -n 100 -r > student_ids.txt
    gshuf -n 100 -r -e math science art > classes.txt
    seq 50 100 | gshuf -n 100 -r > scores.txt
    (
      echo "id class score";
      paste -d " " student_ids.txt classes.txt scores.txt;
    ) | tr ' ' '\t' > report.tsv

Now, with these scores, let's get some aggregate data

    cat report.tsv | datamash -sH --wh --group 2 mean 3 | column -t
     GroupBy(class)  mean(score)
     art             73.214285714286
     math            73.461538461538
     science         72.21875
 

## Generating date sequences

By combining `seq` and `gnu date`, you can generate ranges of dates. On mac, you may need to install 
coreutils to get gdate.

    for i in `seq 10`; do
        date -I --date "2023-08-15 +${i} day" 
    done
     2023-08-16
     2023-08-17
     2023-08-18
     2023-08-19
     2023-08-20
     2023-08-21
     2023-08-22
     2023-08-23
     2023-08-24
     2023-08-25
     
See also [dseq](https://github.com/jeroenjanssens/dsutils/blob/master/dseq)
and another dseq in the [dateutils tool collection](https://github.com/hroptatyr/dateutils)

One common use for date sequences is to identify missing dates. See the section above [join: intersect two files](project:transformation.md#join-intersect-two-files)


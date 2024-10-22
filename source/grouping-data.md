# Grouping Data

## Find distinct items, removing duplicates

    cat data | sort -u

    cat data | sort | uniq

## Find distinct items without sorting

The recipe above relies on a sort. However, sometimes
you know that you dataset will fit in memory, and just want to remove any duplicate items
without the sort. Here are four approaches, from [SO](https://stackoverflow.com/questions/1444406/how-to-delete-duplicate-lines-in-a-file-without-sorting-it-in-unix)


    cat data | awk '!seen[$0]++' file.txt

    cat data | perl -ne'print unless $seen{$_}++'


These first to work by constructing a hashmap that is incremented as each new entry is added, but the magic
lies in the autovivification and post-increment behavior. The 'seen' hash is checked, and only AFTER check
is the value incremented. Both Awk and perl set the initial value of a hash to zero-equivalent value. 

The next approach relies on [datamash](https://www.gnu.org/software/datamash/) which is described later
under [datamash](project:specialized-data-tools.md#datamash)

    cat data | datamash rmdup 1


Another tool that [claims to be faster](https://github.com/koraa/huniq):

    cat data | huniq


## Find duplicate items

    cat data | sort | uniq -d


## Find duplicate items without sorting

This is almost the inverse of the perl approach above:

    cat data | perl -ne'print if ++seen{$_} == 2'

In this case, we increment the value BEFORE we check it.


## Find lines that are in one file, but not in another

Sometimes I have a list of all items, and then a list of items that I want to
remove, and so I need to exclude (subtract) the rejects and work on the
rest.

If both files are sorted (or can be sorted), then you can use either the `comm` utility, or `diff`.

comm takes two **sorted** files, and reports lines that are in a, b or both.

So, to show items that are in `all`, but not in `reject`, tell `comm` to suppress
the lines in the second file (reject, `-2`), and in both files (`-3`):

    comm -2 -3 all reject


See also: `join`, which gives more control on a column by column basis.

You can also grep the output of diff, which is most useful if you want to get a
bit of context around missing lines. Lines removed from the first file are
prefixed with a ' <', or '-' in unified (-u) mode. You'll need to do a little
post-processing on the output to remove the diff characters, so `comm` is often
an easier choice.

    diff -u all keep | egrep '^-' 

If it's not practical to sort the files, then you may need to do a little
actual coding to put the lines from one file into a dictionary or set, and
remove the lines from the other.



## Split data into files based on a field

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

To add a suffix or prefix, use this awk syntax:

    10:51:12 $ awk '{ print $2>($1 ".txt" )}' /tmp/a

Finally, compute an average based on a special purpose program (or your own
one-liner)

    10:51:39 $ for f in 2017*;do  echo -n "$f "; average $f; done;
     2017-11-22 28623.5339943343
     2017-11-23 32164.1470966969
     2017-11-24 41606.0775438271
     2017-11-25 44660.3379886831
     2017-11-26 43758.5492501466
     2017-11-27 43080.1879794521

Naturally, there are other ways to do this specific computation, 
e.g. `cat /tmp/a | datamash -W --group 1 mean 2`, 
but sometimes it's useful to split the files for later processing.

See http://www.theunixschool.com/2012/06/awk-10-examples-to-split-file-into.html for some more examples.



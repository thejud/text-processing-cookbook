# Filter and Select

grep is the linux go-to search tool, supporting fast searching using patterns
and regular expressions.

I'll cover some other options here, and assume a basic understanding of grep
and regular expressions going forward.

## ag - the silver searcher

[ag - AKA the silver searcher](https://github.com/ggreer/the_silver_searcher) is
a fast, flexible alternative to grep forcused on powerful searches with
perl-compatible regular expressions and common default options like recursive
search, avoiding .git files, and a few other nice features.

`brew install the_silver_searcher` or `apt-get install silversearcher-ag`

## ripgrep - a modern search tool

Recently, I have also begun experimenting with
[ripgrep](https://github.com/BurntSushi/ripgrep) which is reportedly faster,
and provides a few nice features like the ability to search within compressed
files.

It is under active development, and I am slowly starting to use it in place
of `ag`.

## searching via perl

perl also has built-in regular expressions, and a few other things that make it
worthwhile. It is installed on most systems by default. Whatever tool you end
up using, it's useful to learn enough of the feature set that you at least know
what is possible, and when a task is likely to be accomplished quickly (e.g.
the top result on stack overflow)

See [General transformation with perl \-pE and \-nE](project:transformation.md)
for using perl as a general purpose filter.

grep (or ag) is great when you want to select lines based on a pattern.
However, sometimes it is useful to select ranges of lines based on their position or by a
delimiter instead.

### select first and last lines

    seq 10 | perl -nE'print if $. == 1 or eof'
     1
     10

This example demonstrates some quirky perl features that are quite useful:

-n loops through the entire input, line by line, without printing anything. 

-E evaluates the given expression for each line, and `-E` (instead of the older `-e`) enables
modern perl features like `say`.

The print function will print the current line by default.

`eof` is the end of the file, and is relatively self-explanatory. What is interesting is that you can print
the last line once eof is detected.

Found an altenative recently that uses the perl flip-flop operator, described below: https://unix.stackexchange.com/a/139199

    seq 10 |  perl -ne 'print if 1..1 or eof'
     1
     10

Similarly, it can be done in awk:

    seq 10 | awk 'NR=1; END {print}'

awk loops through the input, and prints the line if the expression evaluates as
true. Like perl, it also provides BEGIN and END block for special operations
before or after looping through the file. However, in awk, unlike perl, the
last line can be printed in the end block.

Note that all of these methods require reading the entire input, e.g. in a
pipe. If you simply want the first+last line of a file, using head and tail can be
MUCH faster.

    head -1 myfile
    tail -1 myfile

or if you want to sent both lines into another command, you can use a subshell or code block in bash:

    seq 10 > first_ten
    { head -1 first_ten; tail -1 first_ten; } | sort -nr
      10
      1

### range selection with perl's flip-flop (..) operator

Perl has an interesting operator called the range or flip-flop operator that can be used to select ranges of things.

    echo "a b c d e f g" | tr ' ' "\n" | tee letters
     a
     b
     c
     d
     e
     f
     g

Now, let's select everything between the line starting with c, and the line starting with e:

    perl -nE'print if /^c/../^e/' letters
     c
     d
     e

Here we're using perl's bare `print` call to print the entire line based on a
conditional expression. Once whatever is on the left side of the `..` is
matched, the entire expression becomes true (and the line is printed). The
expression becomes false AFTER the right side is matched. Often, regexes are
used on each side, e.g. `print if /^START/../^END/` to print all lines between
START and END. There are a few tips and tricks, described in very gory detail
in the perl docs: https://perldoc.perl.org/perlop.html#Range-Operators

If integers are provided for one or both conditions, it is matched against the
ordinal line number (AKA $.)

    perl -nE'print if 3..5' letters
     c
     d
     e

And, combining both a line number and a pattern, we get:

    perl -nE'print if /^c/..5' letters
     c
     d
     e

And finally, you can continue to the end of the file by using eof (note that it is inclusive):

    perl -nE'print if /^e/..eof' letters
     e
     f
     g

Note that the flip flop operator can turn on and off repeatedly, which you can
use to extract blocks of text separated by a delimiter, or other things:

Here's an example of some data that is delimited by 'START' and 'END'

    cat > delims.txt <<EOF
    START
    1
    2
    END
    4
    5
    6
    START
    7
    END
    8
    9
    START
    10
    11
    12
    END
    13
    14
    15
    EOF

    cat delims.txt | perl -nE'print if /START/../END/'
     START
     1
     2
     END
     START
     7
     END
     START
     10
     11
     12
     END

### Going deeper - Extracting nested fields with the perl flip-flop operator

My friend Robert Stone pointed out that the flip-flop operators can be nested,
and you can use this technique to find nested delimiters. Note that for this to
work, you need to have separate start/end delimters for each section.  

You can use `/start1/../end1/ and /start_inner/../end_inner/` to find start2 within
start1 blocks.

Note that if this gets much more complicated, you will likely be better off using a dedicated parser, but you can go as deep
as you want to!

In this case, we'll parse some simple XML-like structure.

```
cat > outer_inner.text <<EOF
 00
 <OUTER>
	01
   <INNER>
     1
     2
   </INNER>
     30
     40
 </OUTER>
 50
 60
 70
 <OUTER>
   80 
   <INNER>
   4
   5
   </INNER>
   90
 </OUTER>
 100
 EOF
```

And we'll extract the inner parts like this:

```
perl -nE'print if /<OUTER/../<\/OUTER/ and /<INNER/../<\/INNER/' outer_inner.txt
 <INNER>
  1
  2
 </INNER>
 <INNER>
 4
 5
 </INNER>
```

Naturally, if you don't want the tags, you could either filter them out, or filter in: keep only the lines with digits.

# Batch and parallel execution with xargs and parallel

There are a few commands that are generally useful when working with many files.

## xargs 

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
* parameter substitution with `-I %`. If I want multiple replacements, or need to an an extension, that's a good way.

    ls -1 *.sql | xargs -n 1 -I % echo mycommand --logfile %.log %
     mycommand --logfile 201701.csv.log 201701.csv
     mycommand --logfile 201702.csv.log 201702.csv

* parallel execution of commands.

```
# gzip csv files, with four parallel processes.
# print lines as we execute them, and send one file
# at a time to each invocation

ls -t -1 *.csv | xargs -P 4 -t -n 1 gzip   
 gzip 04.csv
 gzip 03.csv
 gzip 02.csv
 gzip 01.csv
```

## GNU parallel

Parallel is a powerful and huge tool, and has many pages of manuals and examples.

However, there are a few key things that I like about running commands via parallel:

* easily create separate log files for each invocation.
* run commands on multiple machines

Here are a few simple examples:

gzip all csv files in a directory. Create one job per core, and provide some diagnostic output.

    ls *.csv | parallel --eta gzip

More complicated, use the command substitution to create a basename, and remove
the extension with an extended command. {} is the input, {.} is the input
without the extension, and {/.} is the basename without the extension.

    ls *.gz | parallel --eta 'mkdir {/.} && cd {/.} && unzip ../{}'

See also: [sem](https://www.gnu.org/software/parallel/sem.html), part of the
gnu parallel package, which allows you to easily limit the number of concurrent
processes without the complexity of parallel. Very useful for running N jobs in
parallel inside a simple for loop.


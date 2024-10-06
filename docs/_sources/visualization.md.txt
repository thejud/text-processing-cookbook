# Visualization

There are a few tools that are useful for quick and dirty visualization.

## Sparklines

[sparklines](https://github.com/deeplook/sparklines) is a small tool (and python module) for quick numeric visualization:

    seq 10 | gshuf | sparklines
   ▂▅▄▃▆▁▇█▃▆


# Misc

## Progress bars in pipes

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


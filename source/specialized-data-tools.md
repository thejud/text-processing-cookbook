# Specialized Tools for Aggregation, Summary, Analysis and Reporting

I use a wide variety of tools for aggregation ranging from relatively simple to
complex and fully featured. Once I have filtered and extracted the data I want,
I have a set of core tools I use for most summarization. Some are small,
single-file scripts that I just copy to a new machine if needed, while others
are full-blown packages.

Note that I won't really talk about actual databases, as the data import/export process usually ends up
being a significant factor (except for csv data via `csvquery`)

The ones that I tend to use most are:

## stats

[stats](https://github.com/hjmangalam/stats/blob/master/stats) is a companion
script to [scut](https://github.com/hjmangalam/scut)
that prints discriptive statistics for a single column of numeric inputs. 

[https://github.com/hjmangalam/scut/blob/master/stats](https://github.com/hjmangalam/scut/blob/master/stats):

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

## csvstat

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

## datamash

do computation and stats on the command line

### quick grouped stats with datamash

For very simple summary stats, I often turn to the `stats` command or
`csvstat`. However, if I want to do a bit more, like aggregate by one or more
columns, [gnu datamash](https://www.gnu.org/software/datamash/manual/datamash.html)
is very useful. It handles large streamed data sets very quickly, and has a
variety of statistical functions available. By default it breaks on tabs. Use
the -W option to break on whitespace. Convert CSV data to TSV transforming data
via `csvformat -T` if you have csv input data.

From the [datamash manual](https://www.gnu.org/software/datamash/manual/datamash.html):

```
# NOTE: apparently the sample data uses tabs, while this example uses whitespace
cat > scores.txt << EOF
Name        Subject          Score
Bryan       Arts             68
Isaiah      Arts             80
Gabriel     Health-Medicine  100
Tysza       Business         92
Zackery     Engineering      54
EOF
```
datamash -W --sort --headers --group 2 mean 3 sstdev 3 < scores.txt

```
GroupBy(Subject)   mean(Score)   sstdev(Score)
Arts               68.9474       10.4215
Business           87.3636       5.18214
Engineering        66.5385       19.8814
Health-Medicine    90.6154       9.22441
Life-Sciences      55.3333       20.606
Social-Sciences    60.2667       17.2273
```

### Cross tables/pivot tables with datamash

    cat <<EOF | csvformat -T > data2.tsv
    year,state,name,amount
    2017,CA,"Foo, Bar",100
    2017,CA,"Boo, Baz",200
    2016,NJ,"Hoo, Dat",75
    2016,CO,"Why, Not",33
    EOF

Create a pivot table that has the year column vs. the state column, summing
the `amount` column for each cell.

    cat data2.tsv | datamash -H crosstab 1,2 sum 4
     GroupBy(year)   GroupBy(state)  sum(amount)
             CA  CO  NJ
     2016    N/A 33  75
     2017    300 N/A N/A


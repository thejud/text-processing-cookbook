# Solutions: Putting it all together

Here are a few more complicated examples that put the various
pieces together.

Note that, as always, there are **many** approaches to each of these, and
I often try to work through each one quickly and iteratively with
small, simple transformations.


## Find available data by user, event class and date

This is a more detailed exploration of the example I showed in the [Introduction](project:introduction.md).

On a project, a coworker asked what dates were available to analyze
in a machine learning project. The data had been collected into S3, grouped
by event class, user, and date. As I knew where the data was stored in S3,
I was able to quickly list the files using an `s3 ls --recursive` command
and store that in a file for quick summarization.

The S3 output was a list of several hundred files approximately like below.
Each line has a creation data, a size, and then the file path that encodes:

- an event class
- a user id
- a date
- the actual filename

```
2024-09-22 139769207 data/class=3002/user=aaa/date=2024-09-21/part-00005
2024-10-04   8235665 data/class=1007/user=aaa/date=2024-10-03/part-00009
2024-10-04     26936 data/class=103006/user=bbb/date=2024-10-03/part-00008
2024-09-13  92385199 data/class=1010/user=aaa/date=2024-09-12/part-00003
2024-10-03  51873127 data/class=1007/user=aaa/date=2024-10-02/part-00001
2024-09-10     52364 data/class=3001/user=aaa/date=2024-09-09/part-00003
2024-09-11  53877463 data/class=1007/user=aaa/date=2024-09-10/part-00001
2024-10-05  36197597 data/class=1007/user=bbb/date=2024-10-04/part-00005
2024-09-14     54249 data/class=103006/user=aaa/date=2024-09-13/part-00000
2024-09-03 146174053 data/class=3002/user=aaa/date=2024-09-02/part-00001
```

I wanted to see the first and last dates available, and have a rough idea if
there were any big gaps by counting the number of dates between the first and last.

Here's the abbreviated output, with the user, event class, first and last date and count of files.

```
user=aaa  class=1007    date=2024-09-05  date=2024-10-05  31
user=aaa  class=3001    date=2024-08-25  date=2024-10-05  42
user=aaa  class=3002    date=2024-08-25  date=2024-10-05  42
user=bbb  class=1007    date=2024-09-30  date=2024-10-05  6
user=bbb  class=3001    date=2024-09-25  date=2024-10-05  11
user=bbb  class=3002    date=2024-09-25  date=2024-10-04  10
```

and here is the transformation I used to summarize the data:

```shell
cat /tmp/files 
    | awk '{print $NF}' \
    | grep user= 
    | perl -pe's/part-.*//'  
    | perl -pe's/.*data\///' 
    | tr / '\t'  
    | sort --uniq
    | datamash --group 2,1 first 3 last 3 count 3
    | column -t
    | sort
```

I'll work through the small (10 line) file list from above for conciseness and
reproducibility. As a result, the final counts will not match the output show
above that used the entire dataset.

So, step by step, the process is as follows: 

1. Grab the filenemame (the last field) from each line

```
| awk '{print $NF}' 
```

produces

```
data/class=1007/user=aaa/date=2024-09-10/part-00001
data/class=1007/user=aaa/date=2024-10-02/part-00001
data/class=1007/user=aaa/date=2024-10-03/part-00009
data/class=1007/user=bbb/date=2024-10-04/part-00005
data/class=1010/user=aaa/date=2024-09-12/part-00003
data/class=103006/user=aaa/date=2024-09-13/part-00000
data/class=103006/user=bbb/date=2024-10-03/part-00008
data/class=3001/user=aaa/date=2024-09-09/part-00003
data/class=3002/user=aaa/date=2024-09-02/part-00001
data/class=3002/user=aaa/date=2024-09-21/part-00005
```

See [Printing the last column, awk and perl](project:extraction.md#printing-the-last-column-awk-and-perl)

2. Next, I filter for lines that contain only the 'user'. It turned out that there were other files, metadata files etc...
that were also present in the s3 output, and so I wanted to filter those out. They were in other directories, not per-user, so
looking for the `user=` string eliminated them. This is an example of "selecting in".

```
| grep user=
```

See [Filter and Select](project:filter-and-select.md)

3. remove the trailing filename

```
| perl -pe's/part-.*//'
```

```
data/class=1007/user=aaa/date=2024-09-10/
data/class=1007/user=aaa/date=2024-10-02/
data/class=1007/user=aaa/date=2024-10-03/
data/class=1007/user=bbb/date=2024-10-04/
data/class=1010/user=aaa/date=2024-09-12/
data/class=103006/user=aaa/date=2024-09-13/
data/class=103006/user=bbb/date=2024-10-03/
data/class=3001/user=aaa/date=2024-09-09/
data/class=3002/user=aaa/date=2024-09-02/
data/class=3002/user=aaa/date=2024-09-21/
```


Each date may have multiple files, but I don't care about individual files . So I'll
trim it. In reality, I have a small script I've written called `dirnames` that
simple strips off the final path portion of each line, from the last `/`, but I
wanted to rely on standard tools for this example, so I remove everything after 'part-'

See [Transformations](project:transformation.md)


4. Remove the `data/` prefix

Remove everything upto and including `data/`. This is a relatively geneneral transformation, and I used the
regular expression because in the actual data I had a few more path components to remove.


```
| perl -pe's/.*data\///' 
```

```
class=1007/user=aaa/date=2024-09-10/
class=1007/user=aaa/date=2024-10-02/
class=1007/user=aaa/date=2024-10-03/
class=1007/user=bbb/date=2024-10-04/
class=1010/user=aaa/date=2024-09-12/
class=103006/user=aaa/date=2024-09-13/
class=103006/user=bbb/date=2024-10-03/
class=3001/user=aaa/date=2024-09-09/
class=3002/user=aaa/date=2024-09-02/
class=3002/user=aaa/date=2024-09-21/
```

See [Transformations](project:transformation.md)

5. split up the directory components by tabs 

I want to have the user, class and date as separate "words" so I can do additional processing. Converting the directory
separator `/` into a tab allows for tools (like datamash) that separate fields by whitespace or tabs.

```
| tr / '\t'  
```

```
class=1007	user=aaa	date=2024-09-10	
class=1007	user=aaa	date=2024-10-02	
class=1007	user=aaa	date=2024-10-03	
class=1007	user=bbb	date=2024-10-04	
class=1010	user=aaa	date=2024-09-12	
class=103006	user=aaa	date=2024-09-13	
class=103006	user=bbb	date=2024-10-03	
class=3001	user=aaa	date=2024-09-09	
class=3002	user=aaa	date=2024-09-02	
class=3002	user=aaa	date=2024-09-21	
```

Naturally, I could have also used perl for this, but `tr` is shorter to type and automatically converts all matches!

Also note that steps 3, 4 and 5 could have all been done by a single, more complicated match and replacement, but I was
working quickly and wanted simple steps I could easily iterate through.


See [Create several simple filters rather than one complicated one](project:transformation.md#create-several-simple-filters-rather-than-one-complicated-one)

6. Sort, and keep only one line per day

```
| sort -u
```

```
class=1007	user=aaa	date=2024-09-10	
class=1007	user=aaa	date=2024-10-02	
class=1007	user=aaa	date=2024-10-03	
class=1007	user=bbb	date=2024-10-04	
class=1010	user=aaa	date=2024-09-12	
class=103006	user=aaa	date=2024-09-13	
class=103006	user=bbb	date=2024-10-03	
class=3001	user=aaa	date=2024-09-09	
class=3002	user=aaa	date=2024-09-02	
class=3002	user=aaa	date=2024-09-21	
```

Because, in step 3 above, I removed the filename, I now had multiple directory lines per day. So, clean that up and
sort the data for the next step.

7. Group by user, and event class, then show the days and counts

Datamash makes it easy to do some quick grouping and aggregations on delimited data, and provides a few useful
text transformations like count, first, last and collapse.

So, because I actually am interested in which users have what data is available, I'm going to change the grouping order

```
| datamash --group 2,1 first 3 last 3 count 3
```

```
user=aaa	class=1007	date=2024-09-10	date=2024-10-03	3
user=bbb	class=1007	date=2024-10-04	date=2024-10-04	1
user=aaa	class=1010	date=2024-09-12	date=2024-09-12	1
user=aaa	class=103006	date=2024-09-13	date=2024-09-13	1
user=bbb	class=103006	date=2024-10-03	date=2024-10-03	1
user=aaa	class=3001	date=2024-09-09	date=2024-09-09	1
user=aaa	class=3002	date=2024-09-02	date=2024-09-21	2
```


See [datamash](project:specialized-data-tools.md#datamash)

8. Pretty print the data into nicer columns for easy viewing/copypaste

```
| column -t
```

```
user=aaa  class=1007    date=2024-09-10  date=2024-10-03  3
user=bbb  class=1007    date=2024-10-04  date=2024-10-04  1
user=aaa  class=1010    date=2024-09-12  date=2024-09-12  1
user=aaa  class=103006  date=2024-09-13  date=2024-09-13  1
user=bbb  class=103006  date=2024-10-03  date=2024-10-03  1
user=aaa  class=3001    date=2024-09-09  date=2024-09-09  1
user=aaa  class=3002    date=2024-09-02  date=2024-09-21  2
```


9. Finally, sort the data correctly so it shows up as desired.

```
| sort
```

```
user=aaa  class=1007    date=2024-09-10  date=2024-10-03  3
user=aaa  class=1010    date=2024-09-12  date=2024-09-12  1
user=aaa  class=103006  date=2024-09-13  date=2024-09-13  1
user=aaa  class=3001    date=2024-09-09  date=2024-09-09  1
user=aaa  class=3002    date=2024-09-02  date=2024-09-21  2
user=bbb  class=1007    date=2024-10-04  date=2024-10-04  1
user=bbb  class=103006  date=2024-10-03  date=2024-10-03  1
```

10. Final steps

After summarizing the data, I determines that the data began arriving on
different days for not only differnt users, but even within different event
classes for the same user.

I did a bit more cleanup (removed the `<field>=`), get a list of all days for each line using the datamash `collapse` aggregator, etc...

Then I was ready to not only answer my coworker's question, but also send a
message to the data ingestion team about the missing days.

At each step in the process, I would typically pipe the output to `head` so I was only getting the top 10 results. That
was enough for me to check each step before processing onto the next, and allowed me to rapidly iterate through the examples.


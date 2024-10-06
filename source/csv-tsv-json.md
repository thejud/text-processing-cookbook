# CSV and TSV

## csvkit

[csvkit](https://csvkit.readthedocs.io/) is an excellent set of tools (and
python libraries) for working with CSV data. I encounter (and generate) a
variety of csv data, and I use many of these frequently. Note that the suite
also works with tab-separated values (TSV). 

I tend to use:

* csvlook - pretty printing of csv files
* csvcut - extract columns from CSV
* csvformat - convert CSV <=> TSV
* csvsql - run SQL queries against CSV data
* csvgrep - search by column in CSV data
* csvstats - summary statistics for CSV file


Here's an introduction:

https://source.opennews.org/articles/eleven-awesome-things-you-can-do-csvkit/

# json

- jq - CLI query language for json. Doesn't handle very large ints.
- jsonpp, json_pp - pretty printing, 
- `python -m json.tool` - pretty printing. Doesn't handle json per lin

## jq

Here's some sample json (created using the [jo json authoring tool](https://github.com/jpmens/jo) )

    { jo user[name]=jud user[id]=17 ; jo user[name]=joe user[id]=22;} | tee json1
    {"user":{"name":"jud","id":17}}
    {"user":{"name":"joe","id":22}}

jq has a fully-featured query language, but since I don't use the more advanced features very often,
I just remember how to index down into object, and print out the raw values:

    # pretty print with colorization
    jq . myfile.json

    # extract user.name from every object
    jq .user.name myfile.json
    "jud"
    "joe"

    # get the raw (unquoted) values.
    jq -r .user.name json1
    jud
    joe

I nearly always use jq for my json needs. However, I've recently been dealing with json that contains very large numeric ids.
Unfortuntely jq rounds large integers.


    echo '{"a":11111222223333344444}' | jq .
    {
      "a": 11111222223333345000
    }

    echo '{"a":11111222223333344444}' | python -m json.tool
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



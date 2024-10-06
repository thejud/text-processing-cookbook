# Extraction

Extraction is a subset of transformation, but it is important enough to have
its own section.

perl, sed and awk are all common tools for both selection and extraction

## Extracting one or more columns with awk

one trivial but common use of awk is to extract column(s) from text with
variable whitespace, like formatted text or the output of a command like `ls -l`:

    ls -l | tail +2 | awk '{print $5}'

To print multiple columns, remember to join with `,`, not ` `:

    ls -l | tail +2 | awk '{print $2,$1}'

## Field extraction via perl -anE 

Perl also has an autosplit mode, -a, which can break up each input line by
whitespace and put it into an array @F. Index the array to pick out columns. Note that the fields are zero-indexed.

    ls -l | perl -anE'say $F[1]'  # the second field


### Printing the last column, awk and perl

Sometimes you just want to print the last column, when you don't know (or don't
want to count) how many columns there are. This is also useful if you have a variable number of columns.

In awk, use the number of fields `$NF` variable:

    ls -l | tail +2 | awk '{print $NF}'

Because perl allows negative array indexing to pick elements, I often use this
to select the last field (or N from the last field), combining it with the autosplit function.

Print the 2nd from the last column:

    ls -l | perl -anE'say $F[-2]'


## Extract simple fields via cut

cut is designed to extract fields from a line, given a single character
delimiter or position list. It will not split on patterns or multi-chararacter
delimiters. Use `awk` or one of the tools described below if you have more
complicated data. By default, it splits fields on a single tab character, but
you can easily specify something else with the `-d' option.


    cat > data <<EOF	
    foo:bar:baz
    fun:stuff:today
    EOF

    cat data | cut -d: -f 1,3
    foo:baz
    fun:today

Note that cut apparently ignores field order:

    cat data | cut -d: -f 3,1
    foo:baz
    fun:today

## Extract by character position with cut

    cat > alpha <<EOF
     abcdef
     gehijk
     EOF

    cat alpha | cut -c '2-4,6'
     bcdf
     ehik

## Extract fixed-width fields with awk

Sometimes you will have fields of known (but possibly different) widths, AKA
fixed width format.

awk can be used to extract the fields (you may need to install gnu awk).
Found this via https://stackoverflow.com/a/28562381

    echo aaaaBBcccccDe | awk '$1=$1' FIELDWIDTHS='4 2 5 1 1' OFS=, 
    aaaa,BB,ccccc,D,e

The `$1=$1` just forces awk to re-parse each line using the FIELDWIDTHDS you've
specified. `OFS` is the output field separator.

Note that this recipe gets every field, and every character between each field.
See the cut recipe above, or the [in2csv approach](#extract-fixed-width-fields-with-in2csv) 
if you only part of each line, or only some fields.

## Extract fixed-width fields with in2csv 

You can also use `in2csv` (part of [csvkit](https://csvkit.readthedocs.io/)) to
convert fixed with to csv files with headers. in2csv requires a schema file, so
this is probably most practical if you find yourself doing this frequently for
the same schema, or there are a LOT of fields and you probably need to iterate
through them anyway.

Define a schema file:

    cat > fields.csv <<EOM
     column,start,length
     name,1,4
     id,5,2
     field1,7,5
     section,12,1
     category,13,1
     EOM

And then use the schema file to extract fixed-width fields:

    echo aaaaBBcccccDe | in2csv -s fields.csv
     name,id,field1,section,category
     aaaa,BB,ccccc,D,e

## Convert whitespace-delimited columns to csv

This can be relatively simple. If you know that you data doesn't contain
any additional commas, you can do a simple substitution:

    # squeeze multiple spaces
    tr -s ' ' ,
    
    perl -pE's/\h+/,/g';  # horizontal space, no newline

    perl -anE'say join(",", @F)'


If you can't be sure that there won't be commas in the fields, you'll want to
do proper quoting. Use a real csv tool. Here's a way to convert to tsv:

    perl -anE'say join("\t", @F)' | csvformat -t -H

    tr -s ' ' '\t' | csvformat -t -H

## cutting columns, other tools

Cutting columns of text is such a common operation that it's worthwhile to have
a few other tools on hand.

## f - trivial field extractor

[f column extractor](https://blog.plover.com/prog/runN.html)

f is a tool with a laser-sharp focus: Extract a single column from a whitespace
delimited file. If you find yourself going often to awk for something like `awk
'{print $3}'`, then add f to your arsenal.

    # quickly extract one column
    printf "the quick brown fox\nand so it goes" | f 3
     brown
     it

Note that supports negative indexes, and can also be used to print the last column.

    seq 10 | paste - - - | f -1  # grab the last column on each line
      3
      6
      9
      10   

## scut - swiss army knife of column cutters

[scut is a better (if slower) cut, extracts arbitrary columns to be selected
based on regexes](https://github.com/hjmangalam/scut)

    # zero indexed, easy to get many columns
    cat data | scut -f '2 1'

    # negative columns are removed
    cat data | scut -f 'ALL -1'

## to extract columns from CSV data, use csvcut

`csvcut` is part of the `csvkit` suite. It allows you to process CSV and TSV files,
and you can specify fields by name or by index.


# Frequency Counts and Distributions

## get a frequency count of items, or find common items

    # pipe into head or tail to get the most or least frequent items
    cat data | sort | uniq -c | sort -nr 

## Find the n most common items

    # find top 7 most common items
    cat data | sort | uniq -c | sort -nr  | head -7

## Better frequency counts

https://github.com/wizzat/distribution

Lets take some random words, repeat each one a random number of times, and then
see what the frequency distribution of the most common words look like:

    cat randwords | perl -ne'$a=$_; print $a for 0..int(rand(25))' | distribution.py
               Key|Ct (Pct)   Histogram
       accelerator|25 (6.05%) ------------------------------------------------------
          absterge|25 (6.05%) ------------------------------------------------------
       Acanthodini|25 (6.05%) ------------------------------------------------------
           Abramis|25 (6.05%) ------------------------------------------------------
       acclimation|24 (5.81%) ---------------------------------------------------
         acatharsy|24 (5.81%) ---------------------------------------------------
      accelerative|23 (5.57%) -------------------------------------------------
    acanthopterous|23 (5.57%) -------------------------------------------------
           Abraham|22 (5.33%) -----------------------------------------------
            Abipon|21 (5.08%) ---------------------------------------------
       accentuable|18 (4.36%) ---------------------------------------
    Acanthocephala|18 (4.36%) ---------------------------------------
            abduce|17 (4.12%) -------------------------------------
              Abba|17 (4.12%) -------------------------------------
            absume|14 (3.39%) ------------------------------    

## Histogram of values

https://github.com/bitly/data_hacks

    pip install data_hacks

Generate 1000 random values from 0-300 and generate a histogram:

    perl -E'say rand(300) for 1..1000' | histogram.py
    # NumSamples = 1000; Min = 0.12; Max = 299.94
    # Mean = 148.416700; Variance = 7602.103173; SD = 87.190041; Median 151.018961
    # each ∎ represents a count of 1
        0.1198 -    30.1021 [   115]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       30.1021 -    60.0845 [    94]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       60.0845 -    90.0668 [   104]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
       90.0668 -   120.0491 [    98]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      120.0491 -   150.0315 [    84]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      150.0315 -   180.0138 [    92]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      180.0138 -   209.9962 [   109]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      209.9962 -   239.9785 [   118]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      239.9785 -   269.9608 [   103]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
      269.9608 -   299.9432 [    83]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎

Note: I removed some of the bucket indicators to make the lines shorter.


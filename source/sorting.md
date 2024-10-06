# Sorting

## gnusort on osx via coreutils

On osx, you will probably want gnusort, which can be installed via `brew install coreutils`
and will then appear as gsort.

### sort items lexicographically, numerically (gnu sort)

    sort
    sort -n

### sort with size units, (k, m, etc)

gnu sort can sort human units, like 10K, 100g.

    du -h | gsort -h -r | head -5
    256K    .
    212K    ./.git
     92K    ./.git/objects
     44K    ./.git/hooks
     20K    ./.git/logs



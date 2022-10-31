#! /bin/bash
for i in 0 1 2 3 4 5 6 7 8
do
    echo "file number $i" >> times.txt
    for j in 0 1 2
    do
        head -n 1 times$j/text$i.txt >> times.txt
    done
done
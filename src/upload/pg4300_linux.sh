#! /bin/bash
# this file runs the Linux experiment on pg4300.txt and creates a result file : pg4300_linux_time.txt
{ time cat pg4300.txt | tr " " "\n" | sort | uniq -c ; } 2>> pg4300_linux_output.txt
tail -n 3 pg4300_linux_output.txt >> pg4300_linux_time.txt
rm pg4300_linux_output.txt
rm pg4300.txt
#!/bin/bash

pc='dta2 dtm1 dtm2 dtm3 dtm4 dtw1 dtw2 dtw3 dtw4 dtw5 dtw6'

job1=$(ssh dtm1 jps | wc -l)
job2=$(ssh dtm2 jps | wc -l)
if [[ $job1 >1 || $job2 >1 ]]; then
  echo 'hadoop沒有關'
  # stopyarn;stophdfs
elif [[ $job1==1 && $job2==1 ]]; then
  echo 'hadoop已經關'
  for n in $pc
    do
    ssh $n sudo poweroff 2>/dev/null
    done
  sudo poweroff
fi

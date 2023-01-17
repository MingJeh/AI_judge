#!/bin/bash
zk_list="dtm3 dtm4 dtm1"

for zk in $zk_list
do
  ssh bigred@"$zk" zkServer.sh start &>/dev/null
  [ "$?" == "0" ] && echo "$zk: zkServer started"
done

ssh bigred@dta1 start-dfs.sh &>/dev/null
[ "$?" == "0" ] && echo "hdfs started"
[ "$?" == "0" ] && ssh bigred@dta1 start-yarn.sh &>/dev/null
[ "$?" == "0" ] && echo "yarn started"
[ "$?" == "0" ] && ssh dtm2 mapred --daemon start historyserver
[ "$?" == "0" ] && echo "dtm2: histortserver started"

hls

yarn rmadmin -getAllServiceState

#!/bin/bash
zk_list="dtm3 dtm4 dtm1"

clusters=$(cat /etc/hosts | grep 'dt' | cut -d' ' -f2)

ssh dtm2 mapred --daemon stop historyserver
[ "$?" == "0" ] && echo "dtm2: histortserver stoped"
[ "$?" == "0" ] && ssh bigred@dta1 stop-yarn.sh &>/dev/null
[ "$?" == "0" ] && echo "yarn stoped"
[ "$?" == "0" ] && ssh bigred@dta1 stop-dfs.sh &>/dev/null
[ "$?" == "0" ] && echo "hdfs stoped"

for zk in $zk_list
do
  ssh bigred@"$zk" zkServer.sh stop &>/dev/null
  [ "$?" == "0" ] && echo "$zk: zkServer stoped"
done

for clu in $clusters 
do
  ssh "$clu" jps
done

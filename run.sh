#!/bin/bash

i=1
j=300
while [ $i -le $j ]
do
  container_name="ao3-proxy-$i"
  host_port=$((61000 + i-1))
  i=$((i+1))
  docker run -d -p $host_port:80 --network=ao3-proxy --ip6="2001:470:c:10f:1145::$i" --name $container_name ao3-proxy-v6:v2
done

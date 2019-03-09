#!/bin/bash
while :
do
    iperf -c 10.0.0.1 -p 6001 -t 600 -b 10M -t 0.17 &
    sleep 1
done
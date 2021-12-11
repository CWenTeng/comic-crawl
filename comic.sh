#!/bin/bash
if [ $1 == "start" ]; then
	PIDS=`ps -ef |grep comicSchedule |grep -v grep | awk '{print $2}'`
	if [ "$PIDS" == "" ]; then
		nohup python3 -u ./comicSchedule.py &
		echo "$!" > pid
		echo "start comic ok. pid:$!"
	else
		echo "comic is already active."
	fi
elif [ $1 == "stop" ]; then
	kill `cat pid`
	echo "stop comic ok."
elif [ $1 == "reload" ]; then
	kill `cat pid`
	echo "stop comic ok."
	PIDS=`ps -ef |grep comicSchedule |grep -v grep | awk '{print $2}'`
	if [ "$PIDS" == "" ]; then
		nohup python3 -u ./comicSchedule.py &
		echo "$!" > pid
		echo "start comic ok. pid:$!"
	else
		echo "comic is already active."
	fi
else
	echo "Please input start or stop or reload."
fi

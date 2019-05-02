ps -ef|grep launch|grep -v grep|awk '{print "kill -9 " $2}'|bash
nohup python3 -u launcher.py &

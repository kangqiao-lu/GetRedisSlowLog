#!/usr/bin/python
#coding=utf-8
import redis
from datetime import datetime
import os,socket,time

"""定义IP PORT 后面for循环读数组，以便扩展,写法:[['192.168.117.211','6379'],['192.168.117.211','6380'],['192.168.117.220','6381']]"""
ip_port = [['192.168.117.211','6379']]

"""获取主机名"""
hostname = socket.gethostname()

"""定义一个获取redis slow log的函数"""
def GetRedisSlowlog(IP,PORT):
        redisClient = redis.StrictRedis(host=IP,port=PORT,db=0)
        slowlog_len = redisClient.execute_command('config','get','slowlog-max-len')[1]
        all_slowlog = redisClient.execute_command('SLOWLOG','GET',slowlog_len)
        redisClient.execute_command('SLOWLOG','RESET')
        now_date = datetime.strftime(datetime.now(),'%Y_%m_%d')
        real_log_file = "/data/mysql/opbin/shell/logs/redis_slow_%s.log" % now_date
        log_file = '/data/mysql/opbin/shell/logs/redis_slow.log'
        os_cmd = "ln -s -f %s %s" % (real_log_file, log_file)
        os.system(os_cmd)
        logfile = open(real_log_file,'a')
        for log in all_slowlog:
                slow_cmd = log[3]
                slow_log = '%s %s %s %s %d %s %s' % (hostname, IP, PORT, datetime.fromtimestamp(log[1]), log[2], slow_cmd[0], slow_cmd[1])
                logfile.write(slow_log + '\n')
        logfile.close()

"""开始获取slowlog"""
while True:
        for i in ip_port:
                GetRedisSlowlog(i[0],i[1])
        time.sleep(60)

import json
import re

import requests
import redis
import time
import sys

from retry import retry

from CarH.ProxyConfig import *
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ProxyError, ConnectionError, Timeout
from CarH.Utils import CPUtils
import socket


class ProxyPool:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=RedisDB['host'], port=RedisDB['port'], db=RedisDB['db'])
        self.Ip_url = Ip_url
        self.max_retry_times = Max_retry_times
        ###可以添加一个清空函数，初始化是清空reids当中的proxies，防止干扰

        self.redis_ = self._get_redis()
        # self._empty_proxies()

        self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self._get_APIproxies, 'interval', minutes=10)
        #保证ip池的活跃性
        self.scheduler.add_job(self.check_active, 'interval', seconds=Check_ipSeconds,id='job1')
        #每隔一段时间来主动获取一些ip
        self.scheduler.add_job(self._get_APIproxies, 'interval', seconds=Get_ipSeconds,id='job2')
        self.scheduler.start()
        self.shutdown_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shutdown_socket.bind(('localhost', Socket_port))
        self.shutdown_socket.listen(1)
        self.utils = CPUtils()

    def _get_redis(self):
        return redis.Redis(connection_pool=self.pool)

    def _empty_proxies(self):
        self.redis_.delete('proxies')
        print('proxies已清空')


    #主要是get请求，几乎没有post请求
    @retry(tries=3,delay=1)
    def get_resopnse(self,url,proxies=None):
        response = requests.get(url,timeout=3,
                                headers=Test_headers,proxies=proxies)
        return response
    def _get_APIproxies(self):
        # 从IP代理商API获取IP代理列表
        response = self.get_resopnse(self.Ip_url)
        #是个列表
        response = response.json()
        if response['code'] == 0:
            #请求成功
            proxies = response['data']
            print(proxies)
            # 将IP代理列表存储到Redis中
            # with self._get_redis() as r:
            for proxy in proxies:
                json_proxies = json.dumps(proxy)
                self.redis_.sadd('proxies', json_proxies)

        elif response['code'] == 111:
            time.sleep(3)
            self._get_APIproxies()
            #提取链接请求太过频繁，超出限制
        elif response['code'] == 113:
            #公网ip改变 白名单未添加/白名单掉了
            current_ip = self.get_resopnse(Ip_url).json()['ip']
            #添加ip白名单
            res = self.get_resopnse(Proxy_white_url+current_ip)
            self.utils(res)
        elif response['code'] == 114:
            self.utils('余额不足')
            pass
            #余额不足
        elif response['code'] == 114:
            self.utils('套餐内IP数量消耗完毕')
            pass
            #套餐内IP数量消耗完毕
        elif response['code'] == 114:
            self.utils('套餐过期')
            pass
            # 套餐过期
        else:
            sys.exit()
            self.utils('代理池异常,进程结束')




    def _check_proxy(self, proxy):
        # 验证IP代理的可用性
        try:
            proxies = {'http': proxy['ip']+str(proxy['port']), 'https': proxy['ip']+str(proxy['port'])}
            response = requests.get(Test_url,proxies=proxies)
            if response.status_code == 200:
                return True
        except (ProxyError, ConnectionError, Timeout)as e:
            print(f"Failed to check proxy {proxy}: {e}")
            pass
        return False


    #验证活性
    def check_active(self):
        # 从Redis中随机获取一个IP代理，并验证其可用性
        print('正在检查代理池活性')
        proxy = self.redis_.srandmember('proxies')
        retry_times = 0
        while not proxy:
            # if not proxy:
            print('当前代理为空')
            # 重新获取代理
            self._get_APIproxies()
            proxy = self.redis_.srandmember('proxies')

        if proxy:
            #代理不为空
            proxy = self.redis_.smembers('proxies')

            for the_proxy in proxy:
                for t in range(self.max_retry_times+1):
                    if not self._check_proxy(json.loads(the_proxy.decode('utf-8'))):
                        retry_times += 1
                        if retry_times > self.max_retry_times:
                            self.redis_.srem('proxies', the_proxy)
                            print('移除-->'+str(the_proxy))
                            retry_times = 0



            pass


    def get_proxy(self):
        proxy = self.redis_.srandmember('proxies')
        while not proxy:
            # 代理池为空，重新获取代理
            self._get_APIproxies()
            proxy = self.redis_.srandmember('proxies')
            print('成功取出' + str(json.loads(proxy.decode('utf-8'))))
            return json.loads(proxy.decode('utf-8'))
        if proxy:
            print('成功取出' + str(json.loads(proxy.decode('utf-8'))))
            return json.loads(proxy.decode('utf-8'))





    def listen_shutdown_command(self):
        while True:
            conn, addr = self.shutdown_socket.accept()
            data = conn.recv(1024)
            if data.decode() == 'shutdown':
                print('接收到暂停命令,定时任务停止')
                self.scheduler.remove_job('job1')
                self.scheduler.remove_job('job2')
                self.scheduler.shutdown()
                break
            else:
                conn.sendall(b'Unknown command')
            conn.close()

    def _delete_proxy(self,proxy):
        '''
        从redis中删除该ip
        :param proxy:
        :return:
        '''
        proxy = re.sub('(.*?)//', '', proxy)
        host, port = proxy.split(':')[0], proxy.split(':')[1]
        _str = f'{{"ip": "{host}", "port": {port}}}'
        self.redis_.srem('proxies', _str)




if __name__ == '__main__':

    pool = ProxyPool()
    # pool.get_proxy()
    # pool.listen_shutdown_command()
    #以上是需要在初始化类时就要执行的操作


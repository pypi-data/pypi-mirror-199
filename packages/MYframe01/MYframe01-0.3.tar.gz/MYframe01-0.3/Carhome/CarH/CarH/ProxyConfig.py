

#配置redis,首先需要启动redis-server
RedisDB = {
    'host': 'localhost',
    'port':6379,
    'db':0,
}

#厂商api
Proxy_url = 'http://127.0.0.1:3333/ip'
neek = '458935'
appkey = '4f43abc76ad62d7974919d49103a4157'
Proxy_white_url = f'https://wapi.http.linkudp.com/index/index/save_white?neek={neek}&appkey={appkey}&white='
#获取ip的api，需要自己登录网站设置（长效，短效，隧道，直连）
# Ip_url = 'http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
Ip_url = 'http://webapi.http.zhimacangku.com/getip?num=3&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='


#每隔多长时间校验一下ip的可用性
Check_ipSeconds = 20
#每隔多长时间主动获取一些ip
Get_ipSeconds = 300


#测试校验
Test_url = 'https://dealer.autohome.com.cn/beijing/0/0/0/0/1/0/0/0.html#pvareaid=2113613'
Test_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
}


Max_retry_times = 3
# Max_retry_delay = 2


# 发件人邮箱账号
My_sender = '206006798@qq.com'
# 发件人邮箱密码（授权码）
My_pass = 'kzrtrfhuvooebhei'
# 收件人邮箱账号
My_user = '206006798@qq.com'


#socket定时任务端口
Socket_port = 2222
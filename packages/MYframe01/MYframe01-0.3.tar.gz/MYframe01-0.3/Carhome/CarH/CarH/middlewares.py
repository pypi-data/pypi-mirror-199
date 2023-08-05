# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import threading
from urllib.parse import urlparse

from scrapy import signals

# useful for handling different item types with a single interface
import logging

logger = logging.getLogger(__name__)
from collections import defaultdict
from CarH.CPProxyPool import ProxyPool

pool = ProxyPool()
# 监听爬虫关闭后提供的信号
my_thread = threading.Thread(target=pool.listen_shutdown_command)
my_thread.start()

class CarhSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self):
        self.is_closing = False

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_closed(self, spider, reason):
        self.is_closing = True


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CarhDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxyMiddleware:
    def __init__(self):
        # pool.check_active()
        # 初始化完成之后，先获取一批ip

        self.failed_count = defaultdict(int)
        self.max_failed = 5

    def process_request(self, request, spider):
        # 随机选择一个代理IP
        proxy = pool.get_proxy()
        proxy = proxy['ip'] + ":" + str(proxy['port'])
        parsed_url = urlparse(request.url)
        if parsed_url.scheme == 'http':
            request.meta['proxy'] = 'http://' + proxy
        elif parsed_url.scheme == 'https':
            request.meta['proxy'] = 'https://' +proxy
        print(request.meta['proxy'])



    def process_response(self, request, response, spider):
        # 获取代理IP
        proxy = request.meta.get('proxy')

        # 判断响应是否成功
        if response.status == 200:
            # 请求成功，将失败次数重置为0
            self.failed_count[proxy] = 0
        else:
            # 请求失败，增加失败次数
            self.failed_count[proxy] += 1

            # 判断失败次数是否达到阈值
            if self.failed_count[proxy] >= self.max_failed:
                self.pool._delete_proxy(proxy)
                spider.logger.info("Removed proxy: %s", proxy)
        return response


#检测cookie是否有效
class CheckStatusMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_response(self, request, response, spider):
        if response.status != 200:
            #如果响应为多少则该cookie失效
            #删除该cookie，将该账号再次登录
            # 做一些特定处理
            pass
        return response

    def spider_closed(self, spider):
        pass
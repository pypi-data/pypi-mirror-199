import logging
from concurrent.futures import ThreadPoolExecutor
import time, datetime
import os
from typing import Optional
from .requestXpath import prequest
logging.basicConfig(format='%(message)s', level=logging.INFO)

prequests = prequest()
class settions:
    workers: Optional[int] = 1
    setting: Optional[dict] = None
    url_queue: Optional[list] = []
    start_urls: Optional[list] = None
    pid = os.getppid()
    request_num: Optional[int] = 0
    success_num: Optional[int] = 0
    false_num: Optional[int] = 0
    start_time: Optional[int] = time.time()
    executor = None

class PrSpiders(settions):
    def __init__(self) -> None:
        PrSpiders.executor = ThreadPoolExecutor(self.workers)
        logging.info('******************PrSpider Start******************')
        if not self.start_urls:
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found ")
        else:
            PrSpiders.start_requests(self)

    def start_requests(cls, **kwargs):
        request = PrSpiders._request(
            cls, callback=cls.parse, url=cls.start_urls)
        PrSpiders.SpiderPool(cls, request, **kwargs)

    @classmethod
    def Requests(cls, url=None, callback=None, headers=None, retry_time=3, method='GET', meta=None,
                 encoding='utf-8', retry_interval=1, timeout=3, **kwargs):
        request = cls._request(cls, callback=callback, url=url)
        PrSpiders.SpiderPool(cls, request, headers=headers, retry_time=retry_time, method=method, meta=meta,
                             encoding=encoding, retry_interval=retry_interval, timeout=timeout, **kwargs)

    def _request(self, callback=None, url=None):
        if isinstance(url, str):
            request = [[url, callback]]
        else:
            request = [[_, callback] for _ in url]
        return request

    @classmethod
    def fetch(self, request, headers=None, retry_time=3, method='GET', meta=None,
              encoding='utf-8', retry_interval=1, timeout=3, **kwargs):
        url = request[0]
        callback = request[1]
        self.request_num += 1
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = prequests.get(url, headers=headers, retry_time=retry_time, method=method, meta=meta,
                                 encoding=encoding, retry_interval=retry_interval, timeout=timeout, **kwargs)
        if response.ok:
            self.success_num += 1
            logging.info(
                f'{current_time} [PrSpider] True [Method] {method} [Num] {self.request_num} [Status] {response.code} [Url] {response.url}')
            return callback(response)
        else:
            self.false_num += 1
            logging.error(
                f'{current_time} [PrSpider] False [Method] {method} [Num] {self.request_num} [Status] {response.code} [Url] {response.url}')

    def SpiderPool(cls, request, **kwargs):
        for _request in request:
            PrSpiders.executor.submit(cls.fetch, _request, **kwargs)

    @classmethod
    def parse(self, response, **kwargs):
        raise NotImplementedError(
            f'{self.__class__.__name__}.parse callback is not defined')

    def process_timestamp(self, t):
        timeArray = time.localtime(int(t))
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return formatTime

    def __del__(self):
        end_time = time.time()
        spend_time = end_time - self.start_time
        m = """
request_num: %s
success_num: %s
false_num: %s
start_time: %s
end_time: %s
spend_time: %.3fs
        """ % (
            self.request_num, self.success_num, self.false_num,
            self.process_timestamp(self.start_time), self.process_timestamp(end_time), spend_time
        )
        logging.info(m)

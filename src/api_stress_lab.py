import requests
from concurrent.futures import ThreadPoolExecutor
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义要测试的 URL
url = 'http://124.71.223.236:8069/shunt-server/api/v1/server/get-url'


# url = 'http://192.168.1.94:8069/shunt-server/api/v1/server/get-url'

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 抛出 HTTP 错误
        return response
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


class ConcurrentAPITester:

    def __init__(self, current_concurrency: int, func):
        if current_concurrency <= 0:
            raise ValueError("current_concurrency must be a positive integer")

        # 响应时间列表
        self.response_times = []

        # 状态码列表
        self.status_codes = []

        # 当前并发量
        self.current_concurrency = current_concurrency

        # 当前并发的接口方法
        self.func = func

    def api_test(self):
        # 记录时间t1
        t1 = time.time()

        # 执行接口方法
        response = self.func(url)
        if response is None:
            return

        # 记录接口返回时间
        response_time = time.time() - t1

        # 收集接口返回时间
        self.response_times.append(response_time)

        # 收集接口返回状态码
        status_code = response.json().get("code", "Unknown")
        self.status_codes.append(status_code)

        # logging.info(f"Response time: {response_time:.2f}s, Status code: {status_code}")

    def run_load_test(self):
        max_workers = self.current_concurrency  # 设置最大并发数
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.api_test) for _ in range(self.current_concurrency)]

        # 等待所有任务完成
        for future in futures:
            future.result()

        # 结果汇总
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        success_rate = (self.status_codes.count(200) / len(self.status_codes)) * 100 if self.status_codes else 0
        logging.info(f"Average response time: {avg_response_time:.2f}s")
        logging.info(f"Success rate: {success_rate:.2f}%")
        logging.info(f"Status codes: {self.status_codes}")
        logging.info("_" * 100)


if __name__ == "__main__":
    # 单次请求测试
    print(fetch_url(url).json())

    # 多次并发测试
    for i in range(2):
        start_time = time.time()
        api_tester = ConcurrentAPITester(current_concurrency=50, func=fetch_url)
        api_tester.run_load_test()
        print(f"Total time taken: {time.time() - start_time:.2f} seconds")

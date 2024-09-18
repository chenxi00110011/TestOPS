import requests
from concurrent.futures import ThreadPoolExecutor
import time

# from tqdm import tqdm

# 定义要测试的 URL
# url = 'http://124.71.223.236:8069/shunt-server/api/v1/server/get-url'
url = 'http://192.168.1.94:8069/shunt-server/api/v1/server/get-url'

# 并发次数
times = 2000

# 创建一个包含 500 个相同 URL 的列表
urls = [url] * times


def fetch_url(url):
    start_t = time.time()
    response = requests.get(url)
    # print(f"Status code for {url}: {response.status_code}")
    assert response.json()['code'] == 200
    assert response.json()['message'] == "成功！"
    assert response.json().get('data').get('url') != ""
    return time.time() - start_t


def main():
    max_workers = times  # 设置最大并发数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]

    # 等待所有任务完成
    for future in futures:
        future.result()


if __name__ == "__main__":
    print(f"最大并发数:{times}")
    for i in range(100):
        start_time = time.time()
        main()
        print(f"Total time taken: {time.time() - start_time:.2f} seconds")

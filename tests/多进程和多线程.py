import os
import time

import requests
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 定义要测试的 URL
url = 'http://p6smessage-cn-cs.p6sai.com:8089/shunt-server/api/v1/server/get-url'

# 创建一个包含 500 个相同 URL 的列表
urls = [url] * 200


def fetch_url(url):
    try:
        response = requests.get(url)
        print(f"Status code for {url}: {response.status_code}")
    except Exception as e:
        print(f"Failed to access {url}: {e}")


def process_urls(chunk):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_url, url) for url in chunk]
        for future in futures:
            future.result()


def main():
    # 获取系统可用的 CPU 核心数
    num_workers = min(os.cpu_count(), len(urls))
    print(f"Using {num_workers} processes (cores)")

    chunk_size = len(urls) // num_workers
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    with Pool(processes=num_workers) as pool:
        with tqdm(total=len(urls), desc="Processing URLs", unit="url", unit_scale=True, leave=True) as pbar:
            results = pool.imap_unordered(process_urls, chunks)
            for _ in results:
                pbar.update(chunk_size)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")

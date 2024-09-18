import requests
from concurrent.futures import ThreadPoolExecutor
import time
from src import user_add, user_login, file_utils

# 读取200个用户信息，并生成列表
file_path = '../data/app_users.txt'  # 替换成你的文件路径
users = file_utils.read_file_lines(file_path)

# 定义要测试的 URL
url = 'http://p6smessage-cn-cs.p6sai.com:8089/shunt-server/api/v1/server/get-url'


def fetch_url(account):
    token = user_login.user_login(account, "123456").json().get("data").get("token")
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
               "token": token}
    data = {"did": "IOTDDD-298852-BMMTC",
            "deviceModel": "T5AI/IPG-5950PCS-AI",
            "boardId": "0x20F1", "iccid": "",
            "versions": "2.2.0-20240911_message",
            "account": account,
            "region": "CN",
            "type": "AD",
            "details": "添加不了\n",
            "contact": "13638601129",
            "problemTime": int(time.time()-3600),
            "pictureUrl": "{\"list\":[]}",
            "allow": 0,
            "lag": "zh_CN"}
    response = user_add.user_add(headers=headers, data=data)
    print(response.json())
    # assert response.json()['code'] == 200


def main():
    max_workers = 10  # 设置最大并发数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, user) for user in users[10:20]]

    # 等待所有任务完成
    for future in futures:
        future.result()


if __name__ == "__main__":
    for i in range(1):
        start_time = time.time()
        main()
        print(f"Total time taken: {time.time() - start_time:.2f} seconds")

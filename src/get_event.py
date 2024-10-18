import time
import requests


def get_event(server: str, port: str):
    return requests.get(
        url="{}:{}/dispose-server/api/v1/msg/get-event?dateTime=2024-09-25&buoyId=-1&channel=all&action=refresh"
            "&timeZone=Asia/Shanghai&type=all&userId=155996&did=IOTFAA-052954-DLRKE".format(server, port)
    )


def concurrency_get_event():
    res = get_event(server="http://p6smessage-cn-cs.p6sai.com", port="8088")
    # res = get_event(server="http://192.168.1.226", port="8082")
    return res


if __name__ == "__main__":
    res = get_event(server="http://p6smessage-cn-cs.p6sai.com", port="8088")
    print(res.json())
    time.sleep(1)

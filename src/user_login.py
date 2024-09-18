import requests


def user_login(account, pwd):
    data = {
        "account": account,
        "pwd": pwd,
        "sn": "4BED294759948BF1AF0F15AF3F09687C"
    }
    res = requests.post(
        url="https://test-erp-cn.p6sai.com/p6s/api/mgr/lite/v1/user-login",
        json=data
    )
    return res


if __name__ == "__main__":
    login = user_login("13638601129", "cx123456")
    print(login.json().get("data").get("token"))
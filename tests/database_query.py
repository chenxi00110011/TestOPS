import mysql.connector


def query_database(host, user, password, database, query):
    """
    连接到 MySQL 数据库并执行 SQL 查询。

    :param host: 数据库服务器地址
    :param user: 用户名
    :param password: 密码
    :param database: 数据库名
    :param query: 要执行的 SQL 查询
    :return: 查询结果
    """
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # 创建游标
        cursor = conn.cursor()

        # 执行 SQL 查询
        cursor.execute(query)

        # 获取查询结果
        rows = cursor.fetchall()

        # 关闭游标和连接
        cursor.close()
        conn.close()

        return rows

    except mysql.connector.Error as err:
        print(f"数据库连接或查询错误: {err}")
        return None


# 使用封装的方法
if __name__ == "__main__":
    import pandas as pd

    # 读取 CSV 文件
    df = pd.read_csv(r"/root/test/plan/t_zw_users_device_right.csv")

    # 获取第一列的数据
    dids = df.iloc[:, 1].tolist()

    # print(dids)

    host = '192.168.1.63'
    user = 'root'
    password = 'P6smsg2024'
    database = 'message-server'
    for did in dids:
        query = f"SELECT COUNT(1) FROM `z_device_store_{did[:6].lower()}_{did[7:9]}` WHERE did ='{did}'"
        # print(query)
        results = query_database(host, user, password, database, query)
        if results:
            for row in results:
                print(did, row, sep="\t")

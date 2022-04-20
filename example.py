"""
------------------------------------------
@File       : example.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2022/4/20 15:55
------------------------------------------
"""
from oracle_pool import OraclePool


def demo():
    cfg = {
        'username': 'maixiaochai',
        'password': 'maixiaochai',
        'host': '192.168.158.1',
        'port': 1521,
        'service_name': 'maixiaochai'
    }

    db = OraclePool(**cfg)

    # 1.不带参数的SQL， fetchall
    sql = "SELECT * FROM MAIXIAOCHAI order by id"
    for no, data in enumerate(db.fetchall(sql), 1):
        print(f"NO.{no} | {data}")

    # 2.带参数的SQL，executemany
    insert_sql = "insert into MAIXIAOCHAI(id, content) values(:1, :2)"
    insert_data = [(1, 'Python'), (2, 'Hello'), (3, 'world')]
    # 这里不用显示commit，自带commit
    db.executemany(insert_sql, insert_data)


if __name__ == "__main__":
    demo()

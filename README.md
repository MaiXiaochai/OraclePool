# OraclePool

---

`Oracle`连接池 (`Oracle Connection Pool`).

##### 基本信息

+ 编程语言 `Python >= 3.5.0`

##### 更新历史：

+ [2019-12-27]
  + 修复一个`Bug`，该`Bug`导致连接池中有且仅有一个连接资源被使用，其余空闲。

+ [2019-05-29]

  + ##### `oracle_conn_pool.py` 文件为主文件。

  + ##### `requirements.txt` 中为所需要的包，使用方法如下

    `pip install -r requirements.txt`

  + ##### 这个只是一个基础的版本，`oracle_conn_pool.py` 内有测试函数，具体的额外的参数修改可以参考类内部的说明
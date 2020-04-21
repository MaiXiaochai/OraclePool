# OraclePool

---

`Oracle`连接池 (`Oracle Connection Pool`).

##### 基本信息

+ 编程语言 `Python >= 3.5.0`
+ 所需库
  + `cx_Oracle`
  + `DBUtils`

##### 更新历史：

**[2020-04-21]**

+ 修复连接用完后，不放回连接池的`bug`
+ 修复使用类名称获取`pool`时的类名称错误(`OrclConnPool`)，改为用`self`
+ 改进了对`config`连接信息的判断逻辑，使得`config`的配置更加简化
+ 改进了新的注释，使用更加清晰
+ 改进了部分代码的格式，使得其更规范
+ 新增`fetch_all`和`fetch_one`
+ 优化了`demo`内容和格式，使得其更规范

**[2020-01-06]**

+ 修复一个`Bug`，该`Bug`导致`fetch_all`执行不带参数的`SQL`时会报错。

  感谢 `CSDN`的[wda406714601](https://me.csdn.net/wda406714601)指出这个BUG。

+ [2019-12-27]
  
+ 修复一个`Bug`，该`Bug`导致连接池中有且仅有一个连接资源被使用，其余空闲。
  
+ [2019-05-29]

  + ##### `oracle_conn_pool.py` 文件为主文件

  + ##### `requirements.txt` 中为所需要的包，使用方法如下

    `pip install -r requirements.txt`

  + ##### 内有测试函数，具体的额外的参数修改可以参考类内部的说明
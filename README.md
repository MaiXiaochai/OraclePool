# OraclePool

---

`Oracle`连接池 (`Oracle Connection Pool`)，单线程多线程都可用

##### 基本信息

+ 编程语言
    + `Python >= 3.9`
+ 所需库
    + `cx_Oracle`

##### 使用方法

+ 参考[example.py](https://github.com/MaiXiaochai/OraclePool/blob/master/example.py)

##### 更新历史：

**[2023-03-27]**

+ 调整默认参数，使得连接池默认为静态连接池。即，最大连接数和最小连接数一致，增长数为0
+ 设置了`getmode=Oracle.SPOOL_ATTRVAL_WAIT`，使得当连接池中没有可用连接时，会等待，而不是报错
+ 添加了大量来自官方文文档的注释，并翻译了其中部分关键内容，解释一些设置的来龙去脉

**[2023-03-17]**

+ pool_size默认值调整为10,并重命名为max_size;
+ 添加min_size参数，默认为1，方便单线程程序使用；
+ 添加threaded=True参数，其本身线程安全，不用额外加锁，大大提升效率;
+ increment默认为1，并且作为可选参数。

**[2022-04-20]**

+ 去掉对`dbutils`的使用，完全使用`cx-oracle`库进行重构
+ 重构后的`Oracle`连接池代码更加简洁，使用更加顺畅
+ 部分方法名进行了微调，与cx-oracle库自身的某些方法名保持一致
    + `fetch_one` -> `fetchone`
    + `fetch_many` -> `fetchmany`
    + `execute_many` -> `executemany`
+ 删去了`execute_sql`方法，合并到`execute`方法中
+ 优化了部分方法的参数，使得其运行更加高效，代码更加简洁
+ 各个方法都自动commit，不用显示调用

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

**[2019-12-27]**

+ 修复一个`Bug`，该`Bug`导致连接池中有且仅有一个连接资源被使用，其余空闲。

**[2019-05-29]**

+ ##### `oracle_conn_pool.py` 文件为主文件

+ ##### `requirements.txt` 中为所需要的包，使用方法如下

  `pip install -r requirements.txt`

+ ##### 内有测试函数，具体的额外的参数修改可以参考类内部的说明
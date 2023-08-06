fly_log
========

最简单的日志，比 print 函数，多了时间与源文件信息。用于比较小的python项目，是适合的。

`from fly_log import debug_print as print, log_time `

特点
========
    功能简单，小的程序非常适用
    与print函数一致，如果影响效率，注释掉相应的代码
    @log_time 打印函数运行的时间，如果影响效率，注释掉相应的代码

安装说明
=======

代码对 Python 3 兼容

* 全自动安装：`pip install fly-log` / `pip3 install fly-log`

代码示例
 
```python
from fly_log import debug_print as print
import time 

def test1():
    print("my fly log ") 

@log_time 
def test2():
    time.sleep(0.5)  

test1()
test2()

# 输出这样的格式
# 2023-03-26 19:50:04.338  test1(fly_log_sample_dev_run.py:6) my fly log 
# 2023-03-26 19:50:04.843  test2() (fly_log_sample_dev_run.py:15) time cost 0.504 sec 
```

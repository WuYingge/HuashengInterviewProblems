# HuashengInterviewProblems
answer for an interview
## 题目一


MyCustomException类定义了一个异常类，可以根据内容打印不同的信息，并包含错误码。
func1 调用func2，func2调用func3，func3抛出的异常，func2捕获后可以做一些处理，然后重新抛出，同理func1也是。

如果每一步不需要特殊处理，func1和func2可以不做捕获，直接完全在main方法里捕获。

前4题结果均在py文件中有所展示

## 题目二

自定义迭代器定义：可以从指定位置开始按照指定步长遍历list

EvenIterable继承StepIterable，遍历列表的偶数位
OddIterable，遍历列表的奇数位

给定列表[1,2,3,4,5,6,7,8,9]，定义新列表类，新增返回奇数迭代器和偶数迭代的方法，用zip打包遍历并输出成对的奇数偶数项

## 题目三
列表的sort和sorted区别主要是在是否修改原始列表
sort会在原地排序，返回None
sorted会返回一个新的排好序的列表，原始列表不动


## 题目四
排序方式如代码所示

## 题目五
简要说下第五题的设计：

采用fastapi + uvicorn实现异步并发实现。
创建一个FastAPI应用，并加载xgboost模型。
用sleep模拟耗时较长的预处理过程，将非异步的函数，统统使用run_in_executor变为非阻塞的，使用backgroundtasks来在后台执行异步任务，并在处理完成后将结果发送回客户端。

当请求参数传来时，首先校验模型是否加载完毕，然后检查参数是否合法，最后开始进入数据预处理和模型预测。
每一步的异常，都会分别抛出不同的异常，返回给客户端。

并发调用采用uvicorn的形式来实现高并发。


资源有限解决办法：
1. 如果是对于CPU比较紧张的情况，可以考虑限制xgboost模型使用的cpu核数。限制uvicorn worker数量。限制请求数量。用uvicorn设置请求超时时间。如果输入值存在大量重复，可以考虑使用缓存机制，不经过预测快速返回结果。

2. 如果是对于内存比较紧张的情况，需要限制worker数量。对请求进行限流。将高耗时的预处理服务和高内存的xgboost预测分开服务，不要每个worker都加载模型，用一个新的服务加载模型，专门做预测服务，预处理独立进行。


代码结构：
- main.py 服务app
- model.py 模型加载
- validator.py 参数校验
- logger.py 日志模块
- common.error_code.py 错误码
- logs 日志目录
- app-admin.sh 启动脚本
- config.yaml 模型配置文件
- model.json 模型文件
- uvicorn_logs.json uvicorn日志配置文件



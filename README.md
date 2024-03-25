# HuashengInterviewProblems
answer for an interview


前4题结果均在py文件中有所展示

简要说下第五题的设计：

采用fastapi + uvicorn实现异步并发实现。
创建一个FastAPI应用，并加载xgboost模型。
用sleep模拟耗时较长的预处理过程，使用asyncio来在后台执行这个任务，并在处理完成后将结果发送回客户端。
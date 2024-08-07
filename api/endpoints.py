# api/endpoints.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()

# 定义 Pydantic 数据模型

class RuntimeInfo(BaseModel):  # 运行时信息
    start_time: datetime  # 爬虫启动时间
    running_time: timedelta  # 爬虫运行总时间
    total_requests: int  # 总请求数
    successful_requests: int  # 成功请求数
    failed_requests: int  # 失败请求数
    average_response_time: float  # 平均响应时间（秒）

class RequestStatistics(BaseModel):  # 请求统计
    timestamp: datetime  # 统计时间点
    total_requests: int  # 总请求数
    successful_requests: int  # 成功请求数
    failed_requests: int  # 失败请求数
    failure_rate: float  # 失败率（百分比）
    requests_per_second: float  # 每秒请求数

class TaskProgress(BaseModel):  # 任务进度
    task_id: str  # 任务ID
    status: str  # 任务状态 (Pending, In Progress, Completed, Failed)
    progress: float  # 任务进度 (0-100%)
    total_items: int  # 总项目数
    completed_items: int  # 已完成项目数
    failed_items: int  # 失败项目数

class ErrorLog(BaseModel):
    timestamp: datetime  # 错误发生时间
    task_id: Optional[str]  # 相关任务ID（如果有）
    error_message: str  # 错误信息
    stack_trace: Optional[str]  # 错误堆栈追踪

class ManualRetry(BaseModel):
    task_id: str  # 任务ID
    retry_count: int  # 重试次数

# 示例数据（通常会从数据库或其他存储中获取）
runtime_info_example = RuntimeInfo(
    start_time=datetime(2024, 7, 30, 8, 0, 0),
    running_time=timedelta(hours=2, minutes=30),
    total_requests=1000,
    successful_requests=950,
    failed_requests=50,
    average_response_time=0.5
)

request_statistics_example = [
    RequestStatistics(
        timestamp=datetime(2024, 7, 30, 10, 30, 0),
        total_requests=1000,
        successful_requests=950,
        failed_requests=50,
        failure_rate=5.0,
        requests_per_second=10.0
    )
]

task_progress_example = TaskProgress(
    task_id="task_12345",
    status="In Progress",
    progress=75.0,
    total_items=100,
    completed_items=75,
    failed_items=5
)

error_logs_example = [
    ErrorLog(
        timestamp=datetime(2024, 7, 30, 10, 0, 0),
        task_id="task_12345",
        error_message="Connection timeout",
        stack_trace="Traceback (most recent call last): ..."
    )
]

# 定义API端点

@router.get("/runtime_info", response_model=RuntimeInfo)
async def get_runtime_info():
    return runtime_info_example

@router.get("/request_statistics", response_model=List[RequestStatistics])
async def get_request_statistics():
    return request_statistics_example

@router.get("/task_progress/{task_id}", response_model=TaskProgress)
async def get_task_progress(task_id: str):
    if task_id == task_progress_example.task_id:
        return task_progress_example
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/error_logs", response_model=List[ErrorLog])
async def get_error_logs():
    return error_logs_example

@router.post("/manual_retry")
async def trigger_manual_retry(retry: ManualRetry):
    # 这里可以加入对重试逻辑的处理
    return {"message": f"Task {retry.task_id} will be retried {retry.retry_count} times"}
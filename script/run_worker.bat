@echo off
setlocal

set workdir=.\

echo workdir: %workdir%
set celery_module=crawler

cd %workdir%

rem 启动 Celery Worker 和 Flower
start /B celery -A %celery_module% worker --loglevel=info
set worker_pid=%!
start /B celery -A %celery_module% flower --port=5555
set flower_pid=%!

rem 等待几秒钟，让进程启动
timeout /t 5 /nobreak >nul

rem 捕获 Ctrl+C (必须手动捕获并执行清理，所以用 goto 来模拟)
:loop
rem 定义清理函数
if not exist NUL (
    echo Stopping Celery Worker and Flower...
    taskkill /F /PID %worker_pid%
    taskkill /F /PID %flower_pid%
    exit /b 0
)
timeout /t 1 /nobreak >nul
goto loop

endlocal
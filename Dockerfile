FROM python:3.10-alpine
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
WORKDIR /app
COPY ./ /app
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt
CMD ["python","script/run_worker.py"]
#CMD ["celery", "-A", "crawler", "worker", "--loglevel=info"]
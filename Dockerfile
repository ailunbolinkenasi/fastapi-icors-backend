FROM docker.io/library/python:3.9.7-alpine as build_env
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && apk add --no-cache libxml2-dev libxml2 libxslt-dev make automake gcc g++ build-base libffi-dev jpeg-dev zlib-dev
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "main.py" ]
FROM docker.io/library/python:3.9.7-alpine as build_env
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && apk add --no-cache libxml2-dev libxml2 libxslt-dev make automake gcc g++ build-base libffi-dev jpeg-dev zlib-dev
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "main.py" ]
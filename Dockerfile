# app/Dockerfile

FROM python:3.9-slim
WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Nara-Ryusei/streamlit.git .
#COPY requirements.txt . ローカルで動かす場合はgit cloneをコメントアウトして、この行を有効にする

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /app

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
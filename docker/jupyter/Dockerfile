FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/usr/src/app

COPY . /app

RUN pip install jupyterlab

EXPOSE 8888

CMD ["jupyter", "lab", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]

FROM python:3.11

RUN mkdir /app/
RUN mkdir -p /app/vectorstore
RUN mkdir -p /app/models

COPY requirements.txt /app/requirements.txt
COPY llm_loader.py /app/
COPY server.py /app/

RUN pip install -r /app/requirements.txt 

WORKDIR /app/
CMD ["python","server.py"]

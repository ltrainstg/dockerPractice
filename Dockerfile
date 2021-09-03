FROM python:3.7-slim

COPY main.py .

RUN pip install fpdf 

CMD ["python", "./main.py"]
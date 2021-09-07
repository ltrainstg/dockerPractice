FROM python:3.7-slim

COPY main.py .
COPY revText.py .
COPY createReport.py .

RUN pip install fpdf 

CMD ["python", "./main.py"]
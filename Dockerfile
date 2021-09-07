FROM python:3.7-slim

LABEL maintainer ="Lionel Duarte" \
      version = "1.0"

COPY main.py .
COPY revText.py .
COPY createReport.py .

RUN pip install fpdf 

CMD ["python", "./main.py"]
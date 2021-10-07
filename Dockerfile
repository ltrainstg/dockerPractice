FROM python:3.8.8

LABEL maintainer ="Lionel Duarte" \
      version = "1.0"
      
COPY ect ect/.   
COPY myMods myMods/.
COPY main.py .
COPY requirments.txt . 


# RUN pip install -r requirments.txt
# RUN apt-get update && apt-get install -y python3 python3-pip


RUN pip3 install requests
RUN pip3 install keyring

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install tqdm

RUN pip3 install fpdf2
RUN pip3 install matplotlib
RUN pip3 install matplotlib_venn
RUN pip3 install scipy



CMD ["python", "./main.py"]

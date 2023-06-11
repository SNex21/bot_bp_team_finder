FROM python:latest

WORKDIR /usr/src/cnw

COPY ./req.txt /usr/src/req.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/req.txt

COPY . usr/src/cnw

EXPOSE 8000
EXPOSE 80

# CMD ["uvicorn", "usr.src.cnw.main:app", "--host=0.0.0.0", "--reload"]

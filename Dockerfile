FROM python:3.9
COPY ./main_project /main_project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /main_project
CMD ["uvicorn","main:app", "--host","0.0.0.0","--port","15400"]

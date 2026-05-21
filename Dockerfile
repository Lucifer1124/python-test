ROM python:3.10-slim
WORKDIR /python
COPY requirements.txt
COPY . .
RUN pip requirements.txt
EXPOSE 4000
CMD ["python", "app.py"]

FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 8501

# cmd to launch app when container is run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
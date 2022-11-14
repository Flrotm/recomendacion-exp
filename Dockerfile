<<<<<<< HEAD
FROM python:3.7 as build

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --compile && rm requirements.txt

FROM python:3.7-slim
RUN groupadd -g 999 python && \
    useradd -r -u 999 python -g python
RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/venv ./venv
COPY --chown=python:python . .

USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
=======
FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
>>>>>>> 99a1b8ae54e72b91d213312b76376ae2032fca3c

EXPOSE 8501

# cmd to launch app when container is run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
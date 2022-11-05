FROM python:alpine
RUN pip3 install flask gunicorn
COPY . /app
WORKDIR app
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "server:app"]

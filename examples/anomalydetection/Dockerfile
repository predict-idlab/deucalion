# syntax=docker/dockerfile:1
# this Dockerfile is for production (building a deucalion sidecar AD application)

FROM python:3.9-slim as runtime

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["main.py"]

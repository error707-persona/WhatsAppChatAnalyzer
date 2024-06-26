# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --requirement requirements.txt && pip cache purge

ARG PORT
EXPOSE ${PORT:-8000}

CMD streamlit run --server.port ${PORT:-8000} main.py
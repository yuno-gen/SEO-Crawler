# Use the official image as base
FROM apache/airflow:2.9.1-python3.12

# Copy a requirements file into the image
COPY requirements.txt /requirements.txt

# Install extra Python deps **as the airflow user** (root‑level pip is blocked)
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

# Copy DAGs last so image rebuilds quickly when code changes
COPY dags /opt/airflow/dags
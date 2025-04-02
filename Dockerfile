FROM python:3.11
WORKDIR /usr/local/app

# making sure to copy in and run requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
# exposing to port 8501
EXPOSE 8501

# adding an app user instead of running root user
RUN useradd -m app
USER app

# have to use commands to run streamlit app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "8501"]
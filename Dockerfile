FROM python:3.13
WORKDIR /usr/local/app

# making sure to copy in and run requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# Copy the .streamlit config folder to change the dark mode and color of buttons
COPY .streamlit ./.streamlit

# exposing to port 8501
EXPOSE 8501

# have to use commands to run streamlit app remember to use -p 8501:8501 if want to run container
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "8501"]
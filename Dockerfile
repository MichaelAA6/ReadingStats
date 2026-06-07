#defines the version python should be run in, slim is used to reduce size
FROM python:3.11-slim
#defines the location of the application
WORKDIR /app
#copy and install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#copy the rest of the application
COPY . .
#expose the port
EXPOSE 5000
#set environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
#command to run the application
CMD ["flask","run"]
#choose an official image
FROM python:3.11-slim

#set working directory in the container
WORKDIR /app

#copy dependencies to the current working directory
COPY requirements.txt .

#install the needed dependencies in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

#copy other application files to the working directory of the container
COPY . .

#run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
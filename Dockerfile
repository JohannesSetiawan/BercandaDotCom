# base image  
FROM python:3.10

ENV PYTHONUNBUFFERED=1

# working at default directory 
WORKDIR .

# copy whole project to your docker home directory. 
COPY . .

# install dependencies  
RUN pip install --upgrade pip  

# run this command to install all dependencies  
RUN pip install -r requirements.txt 

# port where the Django app runs  
EXPOSE 8000
EXPOSE 5432

# start server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
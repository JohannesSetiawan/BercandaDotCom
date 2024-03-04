# base image  
FROM python:3.10

ENV PYTHONUNBUFFERED=1

# working at default directory 
WORKDIR .

# copy whole project to your docker home directory. 
COPY . .

# create virtual environment
CMD ["/bin/bash -c source venv/bin/activate"]

RUN echo "DB_HOST=${{ secrets.DB_HOST }}" > /BercandaAppDotCom/.env \
    && echo "DB_NAME=${{ secrets.DB_NAME }}" >> /BercandaAppDotCom/.env \
    && echo "DJANGO_SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}" >> /BercandaAppDotCom/.env \
    && echo "DEBUG=${{ secrets.DEBUG }}" >> /BercandaAppDotCom/.env \
    && echo "DB_USER=${{ secrets.DB_USER }}" >> /BercandaAppDotCom/.env \
    && echo "DB_PASS=${{ secrets.DB_PASS }}" >> /BercandaAppDotCom/.env 

# install dependencies  
RUN pip install --upgrade pip  

# run this command to install all dependencies  
RUN pip install -r requirements.txt 

# port where the Django app runs  
EXPOSE 8000

# start server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
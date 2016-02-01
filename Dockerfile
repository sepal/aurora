FROM python:3.4.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements_dev.txt
COPY local_settings.example.py /code/local_settings.py
RUN sed -i s:/vagrant/:/code/: local_settings.py
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
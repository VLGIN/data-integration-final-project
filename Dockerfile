FROM apache/airflow:2.3.0
USER root

RUN apt-get update
RUN apt-get install default-libmysqlclient-dev -y
RUN apt-get install gcc -y
RUN sudo pip install mysqlclient
RUN sudo pip install apache-airflow
RUN airflow db upgrade
#RUN airflow db upgrade
#RUN pip install mysqlclient

### whatsupp

This project was started at the [Spring Digital Health Oxford Hack Weekend in May 2016](http://hack.dhox.org).  The overall aim was to bring together publicly available datasources on the safety and content of nutritional supplements, both in order to highlight supplements that contained substances listed on the WADA banned list, and also to help awareness of unexpected, or potentially harmful substances within those supplements for ordinary consumers (non-competitive athletes).  

The code included here looks at the data available on the High Risk list on the US Anti-Doping Agency website - [http://www.supplement411.org/hrl/](http://www.supplement411.org/hrl/).  Supplement411 is published by USADA with list of risks for a number of nutritional supplement, and is governed by terms & conditions, including 'users may not reprint or distribute'.  This code and database has been designed for extracting the data for purposes of analysis and use in a proof-of-concept prototype as part of the whatsupp hack project.

Steps needed to setup:

* Create virtualenv and add required python modules

```
$ pip install -r requirements.txt
``` 

* Create database and tables using sql provided in SQL directory

```
$ mysql

mysql> create database whatsupp;
mysql> create user 'whatsupp_user'@'localhost' identified by 'password';
mysql> grant all privileges on tbtracker.* to 'whatsupp_user'@'localhost';
mysql> flush privileges;

$ mysql whatsupp -u whatsupp_user -p < SQL/whatsupp_database_structure.sql

```

* Create config file and update credentials for new mysql user

```
$ cp config_example.yaml config.yaml
```

* Run scripts to get data and import to new database

```
$ ./scrape_supp411.py
```

# Log Analysis
`log.py` is a python3 program that queries the `news` database and outputs the results on a `HTML` page.

The program aims to answer the following three question:

1. __What are the most popular three articles of all time?__
2. __Who are the most popular three articles of all time?__
3. __On which days did more than 1% of request lead to errors?__

# Quick start

### Download Data
[postgresql "news" database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

### Create a database for the data
```
$ psql
postgres=> create database news;
```

### Add data to new created database
```
psql -d news -f newsdata.sql
```


### Add views to database
```
postgres=> create view number_of_errors_per_day as select L1.time::date, L1.status, count(*) as errors from log L1 where L1.status like '4%' group by 1, 2 order by 1;


postgres=> create view total_number_of_request_per_day as select log.time::date, count(*) as views from log group by 1;
```

### Run program
```
python log.py
```

### view program
open browser on:
```
localhost:8000
```

# Known Issue
After running the program, the command line prints
```
* Serving Flask app "log" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
```
when I try to use the given url `http://0.0.0.0:8000`. I receive an error: _this page can't be reach_.

I suggest accessing the program directly through `localhost:8000`.

# Program Output
### Results:
### The most popular three articles:
* Candidate is jerk, alleges rival -- 338647 views
* Bears love berries, alleges bear -- 253801 views
* Bad things gone, say good people -- 170098 views

### The most popular article authors:
* Ursula La Multa -- 6710940 views
* Rudolf von Treppenwitz -- 3355470 views
* Markoff Chaney -- 1677735 views
* Anonymous Contributor -- 1677735 views

### On which day more than 1% of request lead to errors?
* Jul 17, 2016 -- 2.26 % of errors

# Program written by
[Mario Andres](https://github.com/Marioandres717) for [Udacity - Fullstack Nano Degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)
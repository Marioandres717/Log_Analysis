#!/usr/bin/env python3

import psycopg2
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
DBNAME = "news"

# HTML template from the Query results
HTML_WRAP = '''\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Query Analysis</title>
    </head>
    <body>
        <div>
            <h1>Results:</h1>
            <h2>The most popular three articles:</h2>
            <ul>{}</ul>

            <h2>The most popular article authors:</h2>
            <ul>{}</ul>

            <h2>On which day more than 1% of request lead to errors?</h2>
            <ul>{}</ul>
        </div>
    </body>
</html>
'''

# HTML templates for listing the querie results
popularArticles = '''\
    <li>%s -- %d views</li>
'''

popularAuthors = '''\
     <li>%s -- %d views</li>
'''

requestErrors = '''\
     <li>%s -- %.2f %% of errors</li>
'''


@app.route('/', methods=['GET'])
def main():
    '''Main page of All of the Database query results'''
    articles = ''.join(popularArticles % (title, views)
                       for title, views in get_pop_articles())

    authors = ''.join(popularAuthors % (author, views)
                      for author, views in get_pop_authors())

    request_errors = ''.join(requestErrors % (day, percentage_of_errors)
                             for day, percentage_of_errors
                             in get_days_with_errors_greater_than_1())

    return HTML_WRAP.format(articles, authors, request_errors)


# 'Database code' for the DB news.
def get_pop_articles():
    '''Return all the three most popular articles of all time.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select title, subq.num
    from articles A,
    (select SPLIT_PART(path, '/article/',2) path, count(*) as num
    from log group by path) as subq
    where A.slug = subq.path
    order by num desc
    limit 3
    ''')
    articles = c.fetchall()
    db.close()
    return articles


def get_pop_authors():
    '''Return the most popular authors of all times.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select AU.name, subq2.num
    from authors AU,
    (select subq1.author, count(*) as num
    from log,
    (select author, concat('/articles/', slug) as path
    from articles order by author asc) as subq1
    group by author) as subq2
    where AU.id = subq2.author
    order by subq2.num desc
    ''')
    authors = c.fetchall()
    db.close()
    return authors


def get_days_with_errors_greater_than_1():
    '''Return the days where request in errors are greater than 1%'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select t.day, round(t.percentage_of_errors, 2)
    from (select to_char(T.time, 'Mon dd, yyyy') as day,
    cast(E.errors*100 as numeric) / T.views as percentage_of_errors
    from total_number_of_request_per_day T, number_of_errors_per_day E
    where T.time = E.time) t
    where t.percentage_of_errors > 1
    ''')
    day_with_errors = c.fetchall()
    db.close()
    return day_with_errors


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

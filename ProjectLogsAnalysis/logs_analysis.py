#!/usr/bin/python3

import psycopg2

DATABASE_NAME = "news"


def execute_query_string(query_string):
    try:
        db = psycopg2.connect('dbname=' + DATABASE_NAME)
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        cur = db.cursor()
        cur.execute(query_string)
        res = cur.fetchall()
        db.close()
        return res


def most_popular_articles():
    """Most popular three articles of all time"""

    query_string = """
        SELECT title, count(log.id) AS view
        FROM articles, log
        WHERE log.path = CONCAT('/article/', articles.slug)
        GROUP BY articles.title
        ORDER BY view DESC
        LIMIT 3;
    """

    # Execute query string
    results = execute_query_string(query_string)

    # Present results
    print('1. What are the most popular three articles of all time?')
    for r in results:
        print("\"{}\" @ {} views".format(r[0], str(r[1])))


def most_popular_article_authors():
    """returns top 3 most popular authors"""

    query_string = """
        SELECT name, count(log.id) AS view
        FROM authors
        JOIN articles
        ON authors.id = author
        JOIN log
        ON path LIKE concat('/article/%', articles.slug)
        GROUP BY name
        ORDER BY view DESC
        LIMIT 3;
    """

    # Execute query string
    results = execute_query_string(query_string)

    # Present results
    print('2. Who are the most popular article authors of all time?')
    for r in results:
        print("\"{}\" @ {} views".format(r[0], str(r[1])))


def days_with_requests_erros():
    """returns days with more than 1% errors"""

    query_string = """
        CREATE VIEW error_view AS
        SELECT date_trunc('day', time) "day", count(*) AS requests
        FROM log
        WHERE status LIKE '404%'
        GROUP BY day;

        CREATE VIEW request_view AS
        SELECT date_trunc('day', time) "day", count(*) AS requests
        FROM log
        GROUP BY day;

        SELECT total.day, ROUND(((errors.requests*1.0) / total.requests), 4)
        AS percent
        FROM error_view AS errors
        JOIN request_view AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.requests*1.0) / total.requests), 4) > 0.01)
        ORDER BY percent DESC;
    """

    # Execute query string
    results = execute_query_string(query_string)

    # Present results
    print('3. On which days did more than 1% of requests lead to errors?')
    for r in results:
        date = r[0].strftime('%B %d, %Y')
        error = str(round(r[1] * 100, 1)) + "%" + " errors"
        print("{} - {}".format(date, error))


if __name__ == "__main__":
    print()
    print('Project: Log Analysis')
    print()
    most_popular_articles()
    print()
    most_popular_article_authors()
    print()
    days_with_requests_erros()
    print()

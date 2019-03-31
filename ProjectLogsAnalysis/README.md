### Project: Logs Analysis

The structure of the script is quite straight forward, there are three functions that retreive the answers to the questions.  

Load up and check the database:  
`psql -d news -f newsdata.sql`
`psql -d news`
`psql`

The following views are created within the python script and are here from reference. They provide assistance for the more complicated error question (3).  

```
        CREATE VIEW error_view AS
        SELECT date_trunc('day', time) "day", count(*) AS requests
        FROM log
        WHERE status LIKE '404%'
        GROUP BY day;
```
```
        CREATE VIEW request_view AS
        SELECT date_trunc('day', time) "day", count(*) AS requests
        FROM log
        GROUP BY day;
```

### How to run

Execute the analysis script:  
`$ python3 logs_analysis.py`

### Output sample
```

Project: Log Analysis

1. What are the most popular three articles of all time?
"Candidate is jerk, alleges rival" @ 338647 views
"Bears love berries, alleges bear" @ 253801 views
"Bad things gone, say good people" @ 170098 views

2. Who are the most popular article authors of all time?
"Ursula La Multa" @ 507594 views
"Rudolf von Treppenwitz" @ 423457 views
"Anonymous Contributor" @ 170098 views

3. On which days did more than 1% of requests lead to errors?
July 17, 2016 - 2.3% errors

```

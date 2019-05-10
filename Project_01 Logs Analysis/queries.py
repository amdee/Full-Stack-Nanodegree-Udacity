# List all queries need for the project

popular_articles = """ 
                        SELECT articles.title, COUNT(*) AS num
                        FROM log, articles
                        WHERE log.status = '200 OK'
                        AND articles.slug = substring(log.path, 10)
                        GROUP BY articles.title
                        ORDER BY num DESC
                        LIMIT 3;
                    """

popular_author = """ 
                        SELECT authors.name, COUNT(*) AS num
                        FROM log, articles, authors
                        WHERE log.status = '200 OK'
                        AND authors.id = articles.author
                        AND articles.slug = substring(log.path, 10)
                        GROUP BY authors.name
                        ORDER BY num DESC
                        LIMIT 3;
                    """

request_lead_error = """ 
                            SELECT total.day,
                            ROUND(((errors.error_requests*1.0) / total.requests), 3) AS percent
                            FROM (
                            SELECT date_trunc('day', time) "day", count(*) AS error_requests
                            FROM log
                            WHERE status LIKE '404%'
                            GROUP BY day
                            ) AS errors
                            JOIN (
                            SELECT date_trunc('day', time) "day", count(*) AS requests
                            FROM log
                            GROUP BY day
                            ) AS total
                            ON total.day = errors.day
                            WHERE (ROUND(((errors.error_requests*1.0) / total.requests), 3) > 0.01)
                            ORDER BY percent DESC;
                            
                    """
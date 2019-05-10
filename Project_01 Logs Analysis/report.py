#!/usr/bin/env python3

from __future__ import print_function
import psycopg2
import queries


def query_the_database(query):
    """
    This function connect to the database
    This function query data from database and return result
    :param: query
    :return: result
    """
    try:
        connection = psycopg2.connect("dbname=news")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    except psycopg2.DatabaseError as error:
        print(error, "No connection to the database")


def printing_and_text(arg):
    """
    This function provide a nice printing for assignment
    also a summary text file
    :param arg: queries result
    :return: text.report which contain summary of the answers
    """
    with open('report.txt', 'a') as f:
        if arg == popular_articles:
            print('The most three Popular Articles are:')
            f.write('The most Popular Articles are:\n')
            for i in range(len(arg)):
                result = ' '.join(map(str, (arg[i])))
                result = result[:-1]
                print(i + 1, '.', result, 'views.')
                print(i + 1, '.', result, 'views.', file=f)
            f.write('\n')
            print('\n')
        elif arg == popular_author:
            print('The most three Popular Author are:')
            f.write('The most three Popular Author are:\n')
            for i in range(len(arg)):
                result = ' '.join(map(str, (arg[i])))
                result = result[:-1]
                print(i + 1, '.', result, 'views.')
                print(i + 1, '.', result, 'views.', file=f)
            f.write('\n')
            print('\n')
        elif arg == requests_lead_to_errors:
            print('Days which request lead to more than 1% of errors:')
            f.write(
                'Days which request lead to more than 1% percent of errors:')
            for value in arg:
                print('1. {0:%Y-%m-%d} - {percent:.1f}% errors'
                      .format(value[0], percent=value[1]*100))
                print('\n1. {0:%Y-%m-%d} - {percent:.1f}% errors '
                      .format(value[0], percent=value[1]*100), file=f)


if __name__ == "__main__":
    popular_articles = query_the_database(queries.popular_articles)
    popular_author = query_the_database(queries.popular_author)
    requests_lead_to_errors = query_the_database(queries.request_lead_error)
    queries = [popular_articles, popular_author, requests_lead_to_errors]
    Answer = [printing_and_text(value) for value in queries]


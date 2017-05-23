import sqlite3
from prettytable import PrettyTable

def query_db(database_name, query):
    '''Opens a connections to a SQL database using the sql3lite Python library,
        and runs a provided query on the database.
    Args:
        database_name (string): String containing the name of the database to
         be opened.
        query (string): SQL query to be executed on the database
    Returns:
        tabled_results (PrettyTable object): Results in a table to be printed.
    '''
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    results_generator = cursor.execute(query)

    tabled_results = pprint_results(results_generator)
    return tabled_results

def pprint_results(results_generator):
    ''' Formats results from sql3lite query into a nicer format to be printed.
    Add columns from the sql database, and ascii separators.
    Note: Put all results into memory to construct table.
    Args:
        results_generator (sqlite3.Cursor object): Cursor object containing the
            results after executing a query on it.
    Returns:
        table_output (PrettyTable object): A PrettyTable object containing the
         results of the SQL query in a nicely formatted container.
    '''

    colnames = [colname[0] for colname in results_generator.description]

    table_output = PrettyTable(colnames)
    table_output.padding_width = 1

    for row in results_generator:
         table_output.add_row(row)

    return table_output

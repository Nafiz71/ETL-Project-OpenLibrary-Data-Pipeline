from datetime import datetime, timedelta
import requests
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# 1) Fetch book data from OpenLibrary API
def get_openlibrary_books(num_books, **kwargs):
    ti = kwargs['ti']
    books = []

    # OpenLibrary API: Search for "data engineering" books
    url = f"https://openlibrary.org/search.json?q=data+engineering&limit={num_books}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch books: {e}")
        raise ValueError("Failed to fetch books from OpenLibrary API.")

    data = response.json()

    for doc in data.get('docs', []):
        title = doc.get('title', 'No Title')
        author_list = doc.get('author_name', [])
        author = ", ".join(author_list) if author_list else 'Unknown Author'
        first_publish_year = doc.get('first_publish_year', 'Unknown Year')

        books.append({
            "Title": title,
            "Author": author,
            "Price": "N/A",  # OpenLibrary doesn't provide price
            "Rating": "N/A",  # OpenLibrary doesn't provide rating
            "Year": first_publish_year
        })

    # Convert to DataFrame
    df = pd.DataFrame(books)

    if df.empty:
        raise ValueError("No books found from OpenLibrary.")

    # Push to XCom
    ti.xcom_push(key='book_data', value=df.to_dict('records'))

# 2) Insert fetched book data into Postgres
def insert_book_data_into_postgres(**kwargs):
    ti = kwargs['ti']
    book_data = ti.xcom_pull(key='book_data', task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data found.")

    postgres_hook = PostgresHook(postgres_conn_id='books_connection')
    insert_query = """
    INSERT INTO books (title, authors, price, rating, year)
    VALUES (%s, %s, %s, %s, %s)
    """

    for book in book_data:
        postgres_hook.run(insert_query, parameters=(book['Title'], book['Author'], book['Price'], book['Rating'], book['Year']))

# DAG setup
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetchstore_openlibrary_books',
    default_args=default_args,
    description='Fetch book data from OpenLibrary and store in Postgres',
    schedule=timedelta(days=1),
    catchup=False,
    is_paused_upon_creation=False
)

# Tasks
fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_openlibrary_books,
    op_args=[50],  # Number of books to fetch
    dag=dag,
)

create_table_task = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='books_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT,
        price TEXT,
        rating TEXT,
        year TEXT
    );
    """,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

# Task dependencies
fetch_book_data_task >> create_table_task >> insert_book_data_task

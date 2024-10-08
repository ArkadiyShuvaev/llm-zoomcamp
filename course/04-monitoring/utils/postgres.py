import psycopg2
from psycopg2 import sql
import logging
import os
from datetime import datetime

POSTGRES_DB_PARAMS = {
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'P@ssw0rd!'),
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}


def create_monitoring_db(postgres_db_params: dict):
    default_db_params = postgres_db_params.copy()
    default_db_params['dbname'] = 'postgres'
    try:
        connection = psycopg2.connect(**default_db_params)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{postgres_db_params['dbname']}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                sql.SQL(f"CREATE DATABASE {postgres_db_params['dbname']}"))
            logging.info(
                f"Database {postgres_db_params['dbname']} created successfully!")
        else:
            logging.info(
                f"Database {postgres_db_params['dbname']} already exists!")
        cursor.close()
        connection.close()
    except Exception as error:
        logging.error(f"Error creating database: {error}")


def execute_db_operation(operation_type, POSTGRES_DB_PARAMS, query, params=None):
    try:
        connection = psycopg2.connect(**POSTGRES_DB_PARAMS)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()
        if operation_type == 'create_table':
            logging.info("Table created!")
        else:
            logging.info(
                f"Database operation '{operation_type}' executed successfully!")
    except Exception as error:
        logging.error(f"Error during '{operation_type}': {error}")


def create_chat_table(POSTGRES_DB_PARAMS):
    chat_table_sql = '''
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            session_id VARCHAR,
            message_type VARCHAR,
            content TEXT,
            feedback VARCHAR,
            UNIQUE (session_id, message_type, content)
        )
        '''
    execute_db_operation('create_table', POSTGRES_DB_PARAMS, chat_table_sql)


def create_metrics_table(POSTGRES_DB_PARAMS):
    chat_table_sql = '''
        CREATE TABLE IF NOT EXISTS llm_metrics (
            id SERIAL PRIMARY KEY,
            text_id TEXT,
            cosine_similarity_text_llm_answer NUMERIC,
            negative_llm_answer VARCHAR,
            llm_as_a_judge VARCHAR,
            UNIQUE (text_id)
        )
        '''
    execute_db_operation('create_table', POSTGRES_DB_PARAMS, chat_table_sql)


def save_message_to_db(POSTGRES_DB_PARAMS, session_id, message_type, content, feedback=None):
    insert_query = '''
    INSERT INTO chat_history (timestamp, session_id, message_type, content, feedback)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (session_id, message_type, content)
    DO UPDATE SET feedback = EXCLUDED.feedback
    '''
    params = (datetime.now(), session_id, message_type, content, feedback)
    execute_db_operation('insert', POSTGRES_DB_PARAMS, insert_query, params)


def save_metrics_to_db(POSTGRES_DB_PARAMS, text_id, cosine_similarity=None, negative_answer=None, llm_judge=None):
    insert_query = '''
    INSERT INTO llm_metrics (text_id, cosine_similarity_text_llm_answer, negative_llm_answer, llm_as_a_judge)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (text_id)
    DO UPDATE SET 
        cosine_similarity_text_llm_answer = COALESCE(EXCLUDED.cosine_similarity_text_llm_answer, llm_metrics.cosine_similarity_text_llm_answer),
        negative_llm_answer = COALESCE(EXCLUDED.negative_llm_answer, llm_metrics.negative_llm_answer),
        llm_as_a_judge = COALESCE(EXCLUDED.llm_as_a_judge, llm_metrics.llm_as_a_judge)
    '''
    params = (text_id, cosine_similarity, negative_answer, llm_judge)
    execute_db_operation('insert', POSTGRES_DB_PARAMS, insert_query, params)


def update_feedback_in_db(POSTGRES_DB_PARAMS, session_id, message_type, content, feedback):
    update_query = '''
    UPDATE chat_history
    SET feedback = %s
    WHERE session_id = %s AND message_type = %s AND content = %s
    '''
    params = (feedback, session_id, message_type, content)
    execute_db_operation('update', POSTGRES_DB_PARAMS, update_query, params)

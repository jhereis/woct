import sqlite3

import pandas as pd


INPUT_PATH = "data/processed/reconciliation_results.csv"
DATABASE_PATH = "data/wealth_operations.db"


def load_reconciliation_data():
    return pd.read_csv(INPUT_PATH)


def create_database_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_operations_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS operations (
        operation_id TEXT PRIMARY KEY,
        client_id TEXT,
        operation_type TEXT,
        asset_class TEXT,
        requested_amount REAL,
        currency TEXT,
        request_date TEXT,
        settlement_date TEXT,
        current_status TEXT,
        current_stage TEXT,
        priority TEXT,
        responsible_team TEXT,
        last_update TEXT,
        completion_date TEXT,
        exception_flag BOOLEAN,
        exception_type TEXT,
        severity TEXT,
        source_system TEXT,
        processing_time_hours REAL,
        settlement_lead_time_days REAL,
        sla_status TEXT,
        operational_risk TEXT,
        operation_category TEXT,
        expected_amount REAL,
        processed_amount REAL,
        expected_status TEXT,
        external_status TEXT,
        difference_amount REAL,
        reconciliation_status TEXT
    );
    """

    connection.execute(create_table_query)
    connection.commit()


def load_data_into_database(df, connection):
    df.to_sql(
        "operations",
        connection,
        if_exists="replace",
        index=False,
    )


def validate_database_load(connection):
    query = """
    SELECT COUNT(*) AS total_operations
    FROM operations;
    """

    result = pd.read_sql_query(query, connection)

    print("Total de operações no banco:")
    print(result)


def run_pipeline():
    print("Carregando dados de reconciliação...")

    df = load_reconciliation_data()

    print(f"Registros carregados: {len(df)}")

    connection = create_database_connection()

    create_operations_table(connection)

    load_data_into_database(df, connection)

    validate_database_load(connection)

    connection.close()

    print(f"Banco criado com sucesso: {DATABASE_PATH}")


if __name__ == "__main__":
    run_pipeline()
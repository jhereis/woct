import pandas as pd

INPUT_PATH = "data/raw/operations.csv"
OUTPUT_PATH = "data/processed/operations_enriched.csv"


def load_operations():
    df = pd.read_csv(INPUT_PATH)

    date_columns = [
        "request_date",
        "settlement_date",
        "last_update",
        "completion_date",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def calculate_processing_time(df):
    """
    Calcula o tempo entre o recebimento da operação
    e sua última atualização.
    """

    df["processing_time_hours"] = (
        df["last_update"] - df["request_date"]
    ).dt.total_seconds() / 3600

    df["processing_time_hours"] = (
        df["processing_time_hours"].round(2)
    )

    return df


def calculate_settlement_delay(df):
    """
    Calcula o tempo entre a solicitação e a data prevista
    de liquidação.
    """

    df["settlement_lead_time_days"] = (
        df["settlement_date"] - df["request_date"]
    ).dt.total_seconds() / 86400

    df["settlement_lead_time_days"] = (
        df["settlement_lead_time_days"].round(2)
    )

    return df


def classify_sla(df):
    """
    Classifica as operações com base no tempo de processamento.

    Regras:
    - Até 24 horas: Within SLA
    - Acima de 24 horas: Outside SLA
    """

    df["sla_status"] = df["processing_time_hours"].apply(
        lambda hours: (
            "Within SLA"
            if hours <= 24
            else "Outside SLA"
        )
    )

    return df


def classify_operational_risk(df):
    """
    Identifica operações com maior risco operacional.
    """

    def determine_risk(row):
        if row["current_status"] == "Exception":
            return "Critical"

        if row["severity"] == "Critical":
            return "Critical"

        if row["current_status"] in [
            "Pending Approval",
            "Pending Settlement",
        ]:
            return "High"

        if row["sla_status"] == "Outside SLA":
            return "High"

        if row["priority"] == "Medium":
            return "Medium"

        return "Low"

    df["operational_risk"] = df.apply(
        determine_risk,
        axis=1,
    )

    return df


def classify_operation_status(df):
    """
    Cria uma classificação mais simples para os dashboards.
    """

    def determine_category(status):
        if status in ["Completed", "Reconciled", "Settled"]:
            return "Completed"

        if status in [
            "Received",
            "Validation",
            "Pending Approval",
            "Processing",
            "Pending Settlement",
        ]:
            return "In Progress"

        if status == "Exception":
            return "Exception"

        if status == "Cancelled":
            return "Cancelled"

        return "Other"

    df["operation_category"] = df["current_status"].apply(
        determine_category
    )

    return df


def enrich_operations():
    df = load_operations()

    df = calculate_processing_time(df)
    df = calculate_settlement_delay(df)
    df = classify_sla(df)
    df = classify_operational_risk(df)
    df = classify_operation_status(df)

    return df


def save_enriched_data(df):
    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    print(f"Arquivo enriquecido criado: {OUTPUT_PATH}")
    print(f"Total de registros: {len(df)}")


if __name__ == "__main__":
    enriched_df = enrich_operations()

    save_enriched_data(enriched_df)

    print("\nDistribuição por SLA:")
    print(enriched_df["sla_status"].value_counts())

    print("\nDistribuição por risco operacional:")
    print(enriched_df["operational_risk"].value_counts())

    print("\nDistribuição por categoria:")
    print(enriched_df["operation_category"].value_counts())
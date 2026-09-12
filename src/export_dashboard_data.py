import pandas as pd

OPERATIONS_PATH = "data/processed/operations_enriched.csv"
RECONCILIATION_PATH = "data/processed/reconciliation_results.csv"
OUTPUT_PATH = "data/processed/dashboard_operations.csv"


def export_dashboard_data():
    operations = pd.read_csv(OPERATIONS_PATH)
    reconciliation = pd.read_csv(RECONCILIATION_PATH)

    reconciliation_columns = [
        "operation_id",
        "expected_amount",
        "processed_amount",
        "expected_status",
        "external_status",
        "difference_amount",
        "reconciliation_status",
    ]

    reconciliation = reconciliation[reconciliation_columns]

    dashboard_data = operations.merge(
        reconciliation,
        on="operation_id",
        how="left",
    )

    dashboard_data.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("Arquivo para o dashboard criado com sucesso.")
    print(f"Registros exportados: {len(dashboard_data)}")
    print(f"Arquivo: {OUTPUT_PATH}")


if __name__ == "__main__":
    export_dashboard_data()

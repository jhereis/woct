import random

import pandas as pd

INPUT_PATH = "data/processed/operations_enriched.csv"
OUTPUT_PATH = "data/processed/reconciliation_results.csv"


RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def load_internal_operations():
    return pd.read_csv(INPUT_PATH)


def generate_external_data(df):
    """
    Simula uma base externa de liquidação ou custódia.

    A maioria dos registros será consistente com a base interna,
    mas algumas divergências serão introduzidas intencionalmente.
    """

    external_records = []

    for _, row in df.iterrows():

        operation_id = row["operation_id"]
        requested_amount = row["requested_amount"]
        current_status = row["current_status"]

        expected_amount = requested_amount
        processed_amount = requested_amount
        expected_status = current_status
        external_status = current_status

        scenario = random.choices(
            [
                "Matched",
                "Amount Difference",
                "Status Difference",
                "Missing in External System",
            ],
            weights=[0.82, 0.08, 0.07, 0.03],
            k=1,
        )[0]

        if scenario == "Amount Difference":
            difference = round(
                requested_amount * random.uniform(0.01, 0.05),
                2,
            )

            processed_amount = round(
                requested_amount - difference,
                2,
            )

        elif scenario == "Status Difference":
            external_status = random.choice(
                [
                    "Pending Settlement",
                    "Processing",
                    "Exception",
                ]
            )

        elif scenario == "Missing in External System":
            continue

        external_records.append(
            {
                "operation_id": operation_id,
                "expected_amount": expected_amount,
                "processed_amount": processed_amount,
                "expected_status": expected_status,
                "external_status": external_status,
            }
        )

    return pd.DataFrame(external_records)


def reconcile_operations(internal_df, external_df):
    """
    Compara a base interna com a base externa.
    """

    reconciliation_df = internal_df.merge(
        external_df,
        on="operation_id",
        how="left",
    )

    reconciliation_df["difference_amount"] = (
        reconciliation_df["expected_amount"]
        - reconciliation_df["processed_amount"]
    )

    reconciliation_df["difference_amount"] = (
        reconciliation_df["difference_amount"].fillna(0).round(2)
    )

    def classify_reconciliation(row):

        if pd.isna(row["processed_amount"]):
            return "Missing in External System"

        if abs(row["difference_amount"]) > 0.01:
            return "Amount Difference"

        if row["expected_status"] != row["external_status"]:
            return "Status Difference"

        return "Matched"

    reconciliation_df["reconciliation_status"] = (
        reconciliation_df.apply(
            classify_reconciliation,
            axis=1,
        )
    )

    return reconciliation_df


def save_results(df):
    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    print(f"Arquivo de reconciliação criado: {OUTPUT_PATH}")
    print(f"Total de registros analisados: {len(df)}")


def run_reconciliation():

    internal_df = load_internal_operations()

    external_df = generate_external_data(internal_df)

    reconciliation_df = reconcile_operations(
        internal_df,
        external_df,
    )

    save_results(reconciliation_df)

    print("\nResultado da reconciliação:")
    print(
        reconciliation_df[
            "reconciliation_status"
        ].value_counts()
    )

    print("\nValor total das divergências:")
    print(
        reconciliation_df[
            "difference_amount"
        ].abs().sum()
    )


if __name__ == "__main__":
    run_reconciliation()
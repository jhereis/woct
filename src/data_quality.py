import pandas as pd

INPUT_PATH = "data/raw/operations.csv"


def load_operations():
    return pd.read_csv(INPUT_PATH)


def validate_required_columns(df):
    required_columns = [
        "operation_id",
        "client_id",
        "operation_type",
        "asset_class",
        "requested_amount",
        "currency",
        "request_date",
        "settlement_date",
        "current_status",
        "current_stage",
        "priority",
        "responsible_team",
        "last_update",
        "completion_date",
        "exception_flag",
        "exception_type",
        "severity",
        "source_system",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Colunas ausentes:")
        print(missing_columns)
        return False

    print("Todas as colunas obrigatórias estão presentes.")
    return True


def validate_duplicates(df):
    duplicated_ids = df[df["operation_id"].duplicated()]

    if len(duplicated_ids) > 0:
        print(f"Operações duplicadas encontradas: {len(duplicated_ids)}")
        return False

    print("Nenhuma operação duplicada encontrada.")
    return True


def validate_amounts(df):
    invalid_amounts = df[
        (df["requested_amount"].isna()) |
        (df["requested_amount"] <= 0)
    ]

    if len(invalid_amounts) > 0:
        print(f"Valores inválidos encontrados: {len(invalid_amounts)}")
        return False

    print("Todos os valores financeiros são válidos.")
    return True


def validate_exception_rules(df):
    invalid_exceptions = df[
        (
            df["exception_flag"] == True
        ) &
        (
            df["exception_type"].isna() |
            df["severity"].isna()
        )
    ]

    if len(invalid_exceptions) > 0:
        print(
            "Existem exceções sem tipo ou severidade: "
            f"{len(invalid_exceptions)}"
        )
        return False

    print("As regras de exceção estão válidas.")
    return True


def run_quality_checks():
    df = load_operations()

    print(f"Total de registros analisados: {len(df)}")
    print("-" * 50)

    checks = [
        validate_required_columns(df),
        validate_duplicates(df),
        validate_amounts(df),
        validate_exception_rules(df),
    ]

    print("-" * 50)

    if all(checks):
        print("DATA QUALITY: APROVADO")
    else:
        print("DATA QUALITY: REPROVADO")


if __name__ == "__main__":
    run_quality_checks()
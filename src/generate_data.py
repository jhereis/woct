import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# ============================================================
# CONFIGURAÇÕES
# ============================================================

RANDOM_SEED = 42
NUM_OPERATIONS = 500

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)# ============================================================
# DOMÍNIOS OPERACIONAIS
# ============================================================

OPERATION_TYPES = [
    "Fund Purchase",
    "Fund Redemption",
    "Asset Transfer - Internal",
    "Asset Transfer - External",
    "Cash Transfer",
    "Portfolio Rebalancing",
]

ASSET_CLASSES = [
    "Mutual Fund",
    "Fixed Income",
    "Equity",
    "ETF",
    "Cash",
]

CURRENCIES = ["BRL", "USD"]

STATUSES = [
    "Received",
    "Validation",
    "Pending Approval",
    "Processing",
    "Pending Settlement",
    "Settled",
    "Reconciled",
    "Completed",
    "Exception",
    "Cancelled",
]

STAGES = [
    "Request Received",
    "Data Validation",
    "Approval",
    "Instruction",
    "Processing",
    "Settlement",
    "Reconciliation",
    "Closure",
]

TEAMS = [
    "Operations",
    "Settlement",
    "Client Operations",
    "Middle Office",
    "Reconciliation",
]

EXCEPTION_TYPES = [
    "Missing Documentation",
    "Account Data Mismatch",
    "Asset Position Divergence",
    "Settlement Delay",
    "Approval Pending",
    "Invalid Instruction",
    "Insufficient Position",
    "Duplicate Request",
    "System Processing Error",
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def generate_operation_id(index):
    return f"WM{index:05d}"


def random_datetime(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    return start_date + timedelta(
        days=random_days,
        hours=random.randint(8, 18),
        minutes=random.randint(0, 59),
    )


def generate_amount():
    return round(random.uniform(5_000, 2_000_000), 2)


def generate_status():
    weights = [
        0.08,  # Received
        0.10,  # Validation
        0.06,  # Pending Approval
        0.12,  # Processing
        0.05,  # Pending Settlement
        0.12,  # Settled
        0.08,  # Reconciled
        0.32,  # Completed
        0.05,  # Exception
        0.02,  # Cancelled
    ]

    return random.choices(STATUSES, weights=weights, k=1)[0]


def generate_stage(status):
    status_to_stage = {
        "Received": "Request Received",
        "Validation": "Data Validation",
        "Pending Approval": "Approval",
        "Processing": "Processing",
        "Pending Settlement": "Settlement",
        "Settled": "Settlement",
        "Reconciled": "Reconciliation",
        "Completed": "Closure",
        "Exception": "Processing",
        "Cancelled": "Closure",
    }

    return status_to_stage[status]


def generate_priority(status):
    if status == "Exception":
        return random.choice(["High", "Critical"])

    if status in ["Pending Settlement", "Pending Approval"]:
        return "Medium"

    return "Normal"

# ============================================================
# GERAÇÃO DAS OPERAÇÕES
# ============================================================

def generate_operations(num_operations=NUM_OPERATIONS):

    today = datetime.now()

    start_date = today - timedelta(days=30)
    end_date = today

    records = []

    for index in range(1, num_operations + 1):

        operation_id = generate_operation_id(index)

        status = generate_status()

        request_date = random_datetime(start_date, end_date)

        settlement_date = (
            request_date + timedelta(days=random.randint(1, 5))
        ).date()

        exception_flag = status == "Exception"

        exception_type = (
            random.choice(EXCEPTION_TYPES)
            if exception_flag
            else None
        )

        severity = (
            random.choice(SEVERITIES)
            if exception_flag
            else None
        )

        completion_date = None

        if status in ["Completed", "Reconciled", "Settled"]:
            completion_date = request_date + timedelta(
                days=random.randint(1, 5),
                hours=random.randint(1, 8),
            )

        record = {
            "operation_id": operation_id,
            "client_id": f"CLIENT{random.randint(1, 150):04d}",
            "operation_type": random.choice(OPERATION_TYPES),
            "asset_class": random.choice(ASSET_CLASSES),
            "requested_amount": generate_amount(),
            "currency": random.choice(CURRENCIES),
            "request_date": request_date,
            "settlement_date": settlement_date,
            "current_status": status,
            "current_stage": generate_stage(status),
            "priority": generate_priority(status),
            "responsible_team": random.choice(TEAMS),
            "last_update": request_date + timedelta(
                hours=random.randint(1, 72)
            ),
            "completion_date": completion_date,
            "exception_flag": exception_flag,
            "exception_type": exception_type,
            "severity": severity,
            "source_system": random.choice(
                ["Core Banking", "Trading Platform", "Custody System"]
            ),
        }

        records.append(record)

    return pd.DataFrame(records)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    df_operations = generate_operations()

    output_path = "data/raw/operations.csv"

    df_operations.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    print(f"Arquivo gerado: {output_path}")
    print(f"Total de operações: {len(df_operations)}")
    print("\nDistribuição por status:")
    print(df_operations["current_status"].value_counts())
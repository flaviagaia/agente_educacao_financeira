from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROFILE_PATH = RAW_DIR / "financial_profiles.csv"


DEFAULT_PROFILES = [
    {
        "customer_id": "FIN-1001",
        "name": "Ana Paula Costa",
        "monthly_income": 6800,
        "fixed_expenses": 3900,
        "variable_expenses": 1800,
        "credit_card_debt": 4200,
        "other_debts": 2500,
        "emergency_reserve_months": 0.7,
        "savings_rate_pct": 3.2,
        "credit_card_utilization_pct": 81,
        "missed_payments_6m": 2,
        "recurring_subscriptions": 8,
        "financial_goal": "Montar reserva de emergência de 6 meses",
        "risk_tolerance": "baixa",
    },
    {
        "customer_id": "FIN-1002",
        "name": "Bruno Henrique Lima",
        "monthly_income": 9200,
        "fixed_expenses": 4100,
        "variable_expenses": 2100,
        "credit_card_debt": 1800,
        "other_debts": 0,
        "emergency_reserve_months": 2.8,
        "savings_rate_pct": 11.5,
        "credit_card_utilization_pct": 39,
        "missed_payments_6m": 0,
        "recurring_subscriptions": 5,
        "financial_goal": "Guardar entrada para imóvel em 24 meses",
        "risk_tolerance": "moderada",
    },
    {
        "customer_id": "FIN-1003",
        "name": "Carla Mendes Rocha",
        "monthly_income": 5400,
        "fixed_expenses": 3000,
        "variable_expenses": 1650,
        "credit_card_debt": 3100,
        "other_debts": 4800,
        "emergency_reserve_months": 0.2,
        "savings_rate_pct": 1.1,
        "credit_card_utilization_pct": 92,
        "missed_payments_6m": 3,
        "recurring_subscriptions": 11,
        "financial_goal": "Sair do rotativo e organizar orçamento",
        "risk_tolerance": "baixa",
    },
]


def ensure_sample_data() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not PROFILE_PATH.exists():
        pd.DataFrame(DEFAULT_PROFILES).to_csv(PROFILE_PATH, index=False)
    return pd.read_csv(PROFILE_PATH)


def load_profiles() -> pd.DataFrame:
    return ensure_sample_data()


def load_profile(customer_id: str) -> dict:
    profiles = ensure_sample_data()
    match = profiles.loc[profiles["customer_id"] == customer_id]
    if match.empty:
        raise KeyError(f"Customer id not found: {customer_id}")
    return match.iloc[0].to_dict()

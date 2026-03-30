from __future__ import annotations

import json
from pathlib import Path

from src.agent import ask_financial_education_agent
from src.sample_data import ensure_sample_data


def main() -> None:
    ensure_sample_data()
    result = ask_financial_education_agent(
        customer_id="FIN-1001",
        user_question="Quais prioridades devo atacar primeiro para melhorar minha organizacao financeira?",
    )
    output_path = Path(__file__).resolve().parent / "data" / "processed" / "financial_education_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Agente Educacao Financeira")
    print(f"runtime_mode: {result['runtime_mode']}")
    print(f"customer_id: {result['customer_id']}")
    print(f"monthly_surplus: {result['diagnostics']['monthly_surplus']}")
    print(f"risk_flags: {', '.join(result['diagnostics']['risk_flags'])}")
    print(f"output_path: {output_path}")


if __name__ == "__main__":
    main()

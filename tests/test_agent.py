from __future__ import annotations

import unittest

from src.agent import ask_financial_education_agent
from src.sample_data import ensure_sample_data
from src.tools import build_action_plan, diagnose_financial_health


class FinancialEducationAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        ensure_sample_data()

    def test_diagnostics_return_expected_keys(self) -> None:
        diagnostics = diagnose_financial_health("FIN-1001")
        self.assertIn("monthly_surplus", diagnostics)
        self.assertIn("risk_flags", diagnostics)
        self.assertGreaterEqual(len(diagnostics["risk_flags"]), 1)

    def test_action_plan_has_three_horizons(self) -> None:
        plan = build_action_plan("FIN-1002")
        self.assertIn("plan_30_days", plan)
        self.assertIn("plan_60_days", plan)
        self.assertIn("plan_90_days", plan)

    def test_agent_returns_customer_message(self) -> None:
        result = ask_financial_education_agent(
            customer_id="FIN-1003",
            user_question="Como posso parar de me enrolar com as contas?",
        )
        self.assertIn("runtime_mode", result)
        self.assertIn("customer_message", result)
        self.assertIn("Guardrail", result["customer_message"])


if __name__ == "__main__":
    unittest.main()

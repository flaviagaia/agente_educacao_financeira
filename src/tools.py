from __future__ import annotations

import json
from typing import Any

from .sample_data import load_profile


def get_financial_profile(customer_id: str) -> dict[str, Any]:
    """Retorna o perfil financeiro consolidado do cliente."""
    return load_profile(customer_id)


def diagnose_financial_health(customer_id: str) -> dict[str, Any]:
    """Calcula indicadores sintéticos de saúde financeira para o caso."""
    profile = load_profile(customer_id)
    income = float(profile["monthly_income"])
    committed = float(profile["fixed_expenses"]) + float(profile["variable_expenses"])
    monthly_surplus = income - committed
    debt_total = float(profile["credit_card_debt"]) + float(profile["other_debts"])
    debt_to_income = round(debt_total / income, 4)
    expense_ratio = round(committed / income, 4)

    risk_flags: list[str] = []
    if profile["credit_card_utilization_pct"] >= 75:
        risk_flags.append("utilizacao_alta_cartao")
    if profile["missed_payments_6m"] >= 2:
        risk_flags.append("atrasos_recentes")
    if profile["emergency_reserve_months"] < 1:
        risk_flags.append("reserva_emergencia_baixa")
    if debt_to_income > 0.8:
        risk_flags.append("endividamento_elevado")
    if profile["recurring_subscriptions"] >= 8:
        risk_flags.append("despesas_recorrentes_fragmentadas")

    return {
        "customer_id": customer_id,
        "monthly_surplus": round(monthly_surplus, 2),
        "debt_total": round(debt_total, 2),
        "debt_to_income_ratio": debt_to_income,
        "expense_ratio": expense_ratio,
        "risk_flags": risk_flags,
    }


def explain_financial_priorities(customer_id: str) -> str:
    """Resume os principais focos de educação financeira do cliente."""
    profile = load_profile(customer_id)
    diagnostics = diagnose_financial_health(customer_id)

    priorities: list[str] = []
    if "reserva_emergencia_baixa" in diagnostics["risk_flags"]:
        priorities.append("reconstruir uma reserva mínima antes de assumir novos compromissos")
    if "utilizacao_alta_cartao" in diagnostics["risk_flags"]:
        priorities.append("reduzir a dependência do cartão e do rotativo")
    if "atrasos_recentes" in diagnostics["risk_flags"]:
        priorities.append("estabilizar o calendário de pagamentos")
    if diagnostics["monthly_surplus"] <= 0:
        priorities.append("rever orçamento mensal para voltar ao superávit")
    if not priorities:
        priorities.append("acelerar o plano de médio prazo sem comprometer liquidez")

    return (
        f"O cliente {profile['name']} tem como objetivo principal: {profile['financial_goal']}. "
        f"As prioridades financeiras identificadas são: {', '.join(priorities)}."
    )


def build_action_plan(customer_id: str) -> dict[str, Any]:
    """Gera um plano prático de 30, 60 e 90 dias."""
    profile = load_profile(customer_id)
    diagnostics = diagnose_financial_health(customer_id)
    surplus = diagnostics["monthly_surplus"]

    step_30 = "mapear despesas fixas e variáveis, cancelar recorrências pouco usadas e definir teto semanal de gastos"
    step_60 = "direcionar o excedente para quitar cartão com maior custo efetivo e automatizar contas essenciais"
    if diagnostics["risk_flags"]:
        step_90 = "consolidar reserva inicial de emergência e revisar progresso do objetivo financeiro"
    else:
        step_90 = "acelerar aportes para o objetivo financeiro preservando reserva e disciplina orçamentária"

    estimated_reserve_contribution = max(round(max(surplus, 0) * 0.4, 2), 0)

    return {
        "customer_id": customer_id,
        "plan_30_days": step_30,
        "plan_60_days": step_60,
        "plan_90_days": step_90,
        "estimated_monthly_reserve_contribution": estimated_reserve_contribution,
        "focus_goal": profile["financial_goal"],
    }


def compliance_guardrail(topic: str) -> str:
    """Aplica linguagem segura, educativa e sem aconselhamento formal individual."""
    return (
        "Guardrail de compliance: este agente oferece educação financeira e organização do orçamento, "
        f"não recomendação individual de investimento. Contexto consultado: {topic}."
    )


def build_fallback_report(customer_id: str, user_question: str) -> dict[str, Any]:
    profile = get_financial_profile(customer_id)
    diagnostics = diagnose_financial_health(customer_id)
    explanation = explain_financial_priorities(customer_id)
    plan = build_action_plan(customer_id)
    guardrail = compliance_guardrail(user_question)

    internal_summary = {
        "monthly_surplus": diagnostics["monthly_surplus"],
        "risk_flags": diagnostics["risk_flags"],
        "debt_to_income_ratio": diagnostics["debt_to_income_ratio"],
        "expense_ratio": diagnostics["expense_ratio"],
    }

    customer_message = (
        f"Pergunta do cliente: {user_question}\n\n"
        f"Resumo do perfil:\n{json.dumps(profile, ensure_ascii=False, indent=2)}\n\n"
        f"Diagnóstico:\n{json.dumps(diagnostics, ensure_ascii=False, indent=2)}\n\n"
        f"Explicação:\n{explanation}\n\n"
        f"Plano sugerido:\n{json.dumps(plan, ensure_ascii=False, indent=2)}\n\n"
        f"{guardrail}"
    )

    return {
        "customer_id": customer_id,
        "profile": profile,
        "diagnostics": diagnostics,
        "explanation": explanation,
        "action_plan": plan,
        "guardrail": guardrail,
        "customer_message": customer_message,
        "internal_summary": internal_summary,
    }

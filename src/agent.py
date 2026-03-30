from __future__ import annotations

import asyncio
import os
from typing import Any

from .tools import build_fallback_report

try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.messages import TextMessage
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_ext.models.openai import OpenAIChatCompletionClient
except Exception:  # pragma: no cover - optional runtime dependency
    AssistantAgent = None
    TextMessage = None
    RoundRobinGroupChat = None
    OpenAIChatCompletionClient = None


AUTOGEN_SYSTEM_CONTEXT = {
    "diagnostic_agent": (
        "Você é um agente analista financeiro. Seu trabalho é interpretar o perfil, identificar excesso de "
        "comprometimento de renda, reserva insuficiente e sinais de atraso, sem inventar dados."
    ),
    "education_agent": (
        "Você é um agente de educação financeira. Explique de forma clara, não julgadora, e sempre rotule "
        "o conteúdo como educativo."
    ),
    "planner_agent": (
        "Você é um agente de plano de ação. Organize recomendações de curto prazo em 30, 60 e 90 dias, "
        "sempre com foco em orçamento, dívida e reserva."
    ),
}


def _build_agent_runtime(model_name: str = "gpt-4.1-mini"):
    if not (AssistantAgent and RoundRobinGroupChat and OpenAIChatCompletionClient and os.getenv("OPENAI_API_KEY")):
        return None

    client = OpenAIChatCompletionClient(model=model_name, api_key=os.getenv("OPENAI_API_KEY"))
    diagnostic_agent = AssistantAgent(
        name="diagnostic_agent",
        model_client=client,
        system_message=AUTOGEN_SYSTEM_CONTEXT["diagnostic_agent"],
    )
    education_agent = AssistantAgent(
        name="education_agent",
        model_client=client,
        system_message=AUTOGEN_SYSTEM_CONTEXT["education_agent"],
    )
    planner_agent = AssistantAgent(
        name="planner_agent",
        model_client=client,
        system_message=AUTOGEN_SYSTEM_CONTEXT["planner_agent"],
    )
    return RoundRobinGroupChat([diagnostic_agent, education_agent, planner_agent])


async def _run_autogen(customer_id: str, user_question: str, model_name: str) -> dict[str, Any]:
    runtime = _build_agent_runtime(model_name=model_name)
    if runtime is None:
        report = build_fallback_report(customer_id=customer_id, user_question=user_question)
        return {"runtime_mode": "deterministic_fallback", **report}

    prompt = (
        f"customer_id={customer_id}\n"
        f"user_question={user_question}\n"
        "Use raciocínio multiagente para produzir: diagnóstico, explicação educativa, plano de ação e guardrail."
    )
    result = await runtime.run(task=prompt)
    messages = getattr(result, "messages", [])
    final_text = ""
    for message in reversed(messages):
        content = getattr(message, "content", "")
        if content:
            final_text = str(content)
            break

    report = build_fallback_report(customer_id=customer_id, user_question=user_question)
    report["customer_message"] = final_text or report["customer_message"]
    return {"runtime_mode": "autogen_groupchat", **report}


def ask_financial_education_agent(
    customer_id: str,
    user_question: str,
    model_name: str = "gpt-4.1-mini",
) -> dict[str, Any]:
    return asyncio.run(_run_autogen(customer_id=customer_id, user_question=user_question, model_name=model_name))

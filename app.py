from __future__ import annotations

import streamlit as st

from src.agent import ask_financial_education_agent
from src.sample_data import load_profiles


st.set_page_config(page_title="Agente de Educacao Financeira", layout="wide")
st.title("Agente de Educacao Financeira")
st.caption("MVP com Microsoft AutoGen para diagnostico financeiro, educacao e plano de acao.")

profiles = load_profiles()
profile_options = profiles.set_index("customer_id")["name"].to_dict()

with st.sidebar:
    st.header("Stack Tecnica")
    st.markdown(
        """
        - `Microsoft AutoGen` para orquestracao multiagente
        - `AssistantAgent` e `RoundRobinGroupChat` como topologia prevista
        - fallback deterministico para execucao local sem credenciais
        - `Streamlit` para inspecao do runtime e dos artefatos
        """
    )
    st.header("Premissas do MVP")
    st.markdown(
        """
        - educacao financeira, nao consultoria de investimentos
        - analise baseada em perfil demo estruturado
        - plano de acao em `30/60/90 dias`
        - guardrail explicito de compliance
        """
    )

customer_id = st.selectbox(
    "Selecione o cliente",
    options=list(profile_options.keys()),
    format_func=lambda cid: f"{cid} - {profile_options[cid]}",
)

default_question = "Como posso organizar melhor meu orçamento e sair da pressão do cartão?"
user_question = st.text_area("Pergunta do cliente", value=default_question, height=120)

if st.button("Executar agente", type="primary"):
    result = ask_financial_education_agent(customer_id=customer_id, user_question=user_question)

    col1, col2, col3 = st.columns(3)
    col1.metric("Runtime mode", result["runtime_mode"])
    col2.metric("Superávit mensal", f"R$ {result['diagnostics']['monthly_surplus']:.2f}")
    col3.metric("Dívida / renda", f"{result['diagnostics']['debt_to_income_ratio']:.2%}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Mensagem ao cliente", "Diagnóstico", "Plano 30/60/90", "Perfil estruturado"]
    )
    with tab1:
        st.markdown(result["customer_message"])
        st.info(result["guardrail"])
    with tab2:
        st.subheader("Explicação das prioridades")
        st.write(result["explanation"])
        st.json(result["diagnostics"])
    with tab3:
        st.json(result["action_plan"])
    with tab4:
        st.json(result["profile"])

st.divider()
st.subheader("Arquitetura resumida")
st.code(
    """Cliente -> AutoGen orchestrator -> DiagnosticAgent -> EducationAgent -> PlannerAgent -> resposta final
                 \\-> fallback deterministico local (sem OPENAI_API_KEY)""",
    language="text",
)

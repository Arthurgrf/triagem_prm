import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Triagem de PRM", page_icon="💊", layout="centered")

st.title("💊 Triagem Clínica de PRM")
st.markdown("Insira uma breve descrição do caso do paciente para identificar a possível presença de **Problemas Relacionados a Medicamentos (PRM 1 a 7)**.")

# Campo para a chave da API
api_key = st.sidebar.text_input("Cole sua API Key do Gemini aqui:", type="password")

# Instruções para o Modelo de IA
SYSTEM_PROMPT = """
Você é um especialista em Farmácia Clínica e Farmacovigilância.
Sua tarefa é analisar o relato de um caso clínico e identificar a presença de Problemas Relacionados a Medicamentos (PRM) com base no Consenso de Granada / Método Dáder.

As categorias são:
- PRM 1 (Necessidade): Não usa o medicamento de que necessita.
- PRM 2 (Necessidade): Usa um medicamento de que não necessita.
- PRM 3 (Efetividade): Inefetividade não quantitativa (não responde ao tratamento).
- PRM 4 (Efetividade): Inefetividade quantitativa (subdose/posologia inferior).
- PRM 5 (Segurança): Insegurança quantitativa (overdose/toxicidade/dose elevada).
- PRM 6 (Segurança): Insegurança não quantitativa (Reação Adversa ao Medicamento - RAM).
- PRM 7 (Outros/Adesão): Problema decorrente de não adesão ou erro de administração.

Resposta desejada:
1. Destaque o PRM Principal Detectado (ex: "PRM 6 - Reação Adversa ao Medicamento").
2. Liste o(s) Medicamento(s) Envolvido(s).
3. Justificativa Clínica Resumida (por que este PRM foi escolhido?).
4. Sugestão de Conduta Farmacoterapêutica (de forma objetiva).

Se o relato for insuficiente, solicite mais dados clínicos.
Mantenha um tom profissional, direto e claro.
"""

# Formulário no Streamlit
relato = st.text_area("Descrição do Caso Clínico:", height=180, placeholder="Ex: Paciente 60 anos, em uso de Enalapril 20mg/dia. Relata tosse seca há 2 semanas...")

if st.button("🔍 Analisar Caso", type="primary"):
    if not api_key:
        st.error("Por favor, insira uma API Key do Gemini no menu lateral para continuar.")
    elif not relato.strip():
        st.warning("Por favor, digite o relato do caso antes de analisar.")
    else:
        try:
            # 1. Cria o cliente com a API Key usando o SDK moderno
            client = genai.Client(api_key=api_key)

            # 2. Chama o modelo ativo gemini-2.5-flash
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT}\n\nRelato do caso:\n{relato}"
            )

            # 3. Exibe o resultado
            st.success("Análise Concluída!")
            st.markdown("---")
            st.markdown(response.text)
            st.caption("⚠️ Nota: Esta ferramenta é um sistema de apoio à decisão clínica e não substitui o julgamento do profissional de saúde.")

        except Exception as e:
            st.error(f"Erro ao processar a requisição: {e}")

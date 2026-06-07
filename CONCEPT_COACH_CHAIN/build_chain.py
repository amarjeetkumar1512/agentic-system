from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama


def build_chain():
    system_message = (
        "You are a beginner-friendly programming instructor. "
        "Always respond in valid JSON with keys: concept, analogy, explanation, key_takeaway."
    )

    human_message = (
        "Explain {topic} using an analogy from {analogy_domain}."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message)
    ])

    llm = ChatOllama(
        model="qwen:1.8b",
        base_url="http://localhost:11434",
        temperature=1,
        num_predict=120
    )

    parser = JsonOutputParser()

    return prompt | llm | parser
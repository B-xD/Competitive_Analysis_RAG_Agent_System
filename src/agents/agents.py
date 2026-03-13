
from langgraph.prebuilt import create_react_agent
from ..config import llm
from ..tools import suggest_questions, fetch_search_results, store_in_chromadb, generate_report
from langchain_core.messages import SystemMessage

question_generator_agent = create_react_agent(
    model =llm,
    tools = [suggest_questions],
    prompt = SystemMessage(content = """
    You are a competitive analysis question generator.
    Use the suggest_questions tool to generate targeted competitive analysis questions
    for the given company. Return the structured output as provided by the tool.


    """)
)

data_retrieval_storage_agent = create_react_agent(
    model=llm,
    tools=[fetch_search_results, store_in_chromadb],
    prompt=(
        "You are a data retrieval and storage agent. "
        "First, use the fetch_search_results tool to retrieve answers for the provided questions. "
        "Then, use the store_in_chromadb tool to persist the question-answer pairs into the vector store. "
        "Return the storage status when complete."
    )
)

report_drafter_agent = create_react_agent(
    model=llm,
    tools=[generate_report],
    prompt=(
        "You are a competitive intelligence report writer. "
        "Use the generate_report tool to build a structured prompt template for the given company and sector. "
        "Return the prompt template for downstream RAG invocation."
    )
)
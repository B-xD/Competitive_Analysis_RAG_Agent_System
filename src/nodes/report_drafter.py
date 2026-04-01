from ..state import CompetitiveAnalysisState
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import llm 
from ..agents import report_drafter_agent
from ..tools import generate_report
from langchain_core.prompts import ChatPromptTemplate
from ..config import tictoc

import json 

def run_report_drafter(state: CompetitiveAnalysisState) -> CompetitiveAnalysisState:
    """
    Node: Generates the final competitive analysis report using RAG.
    Retrieves stored Q&A context from ChromaDB and invokes the report generation prompt.

    Args:
        state: The current CompetitiveAnalysisState object.

    Returns:
        Updated CompetitiveAnalysisState with the final report.
    """
    print("=" * 60)
    print(f"[NODE] run_report_drafter | Company: {state.company_name}")
    print("=" * 60)

    try:
        # reate retriever from vector store
        retriever = state.vectorstore.as_retriever(
            search_kwargs={"k": 10}
        )

        # Query retriever for competitive analysis documents
        query = f"competitive analysis for {state.company_name}"
        retrieved_docs = retriever.invoke(query)
        print(f"[RETRIEVER] Documents retrieved: {len(retrieved_docs)}")

        # Handle empty retrieval
        if not retrieved_docs:
            print("[WARNING]: No documents retrieved from vector store.")
            state.error_message = "No documents retrieved from ChromaDB for report generation."
            state.report        = "Report could not be generated: no context available."
            return state

        # Concatenate page_content into single context string
        context = "\n\n".join([
            doc.page_content for doc in retrieved_docs if doc.page_content.strip()
        ])
        print(f"[CONTEXT] Total context length: {len(context)} characters")

        # Invoke generate_report tool to get ChatPromptTemplate
        prompt_template = generate_report.invoke({
            "company_name": state.company_name,
            "sector":       state.sector or "General"
        })

        # Validate returned object is a ChatPromptTemplate
        if not isinstance(prompt_template, ChatPromptTemplate):
            print(f"[ERROR]: generate_report returned unexpected type: {type(prompt_template)}")
            state.error_message = (
                f"generate_report returned {type(prompt_template)} instead of ChatPromptTemplate."
            )
            state.report = "Report could not be generated: invalid prompt template."
            return state

        # Compose chain and invoke with retrieved context
        chain  = prompt_template | llm
        result = chain.invoke({
            "company_name": state.company_name,
            "sector":       state.sector or "General",
            "context":      context
        })

        # Extract and store the report
        state.report = result.content if hasattr(result, "content") else str(result)

        # Log a brief preview
        preview = state.report[:300].replace("\n", " ")
        print(f"[REPORT PREVIEW]: {preview}...")
        print(f"[STATE] Report length: {len(state.report)} characters")

    except Exception as e:
        print(f"[ERROR]: run_report_drafter failed: {str(e)}")
        state.error_message = f"run_report_drafter error: {str(e)}"
        state.report        = f"Report generation failed due to an error: {str(e)}"

    return state
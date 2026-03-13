from ..state import CompetitiveAnalysisState
from langchain_core.messages import HumanMessage, SystemMessage
from ..agents import data_retrieval_storage_agent 
import json 

# run_data_retrieval_storage node
def run_data_retrieval_storage(state: CompetitiveAnalysisState) -> CompetitiveAnalysisState:
    """
    Node: Fetches search results for generated questions and stores them in ChromaDB.
    Parses the agent response to update qna_results and chromadb_insert_status in state.

    Args:
        state: The current CompetitiveAnalysisState object.

    Returns:
        Updated CompetitiveAnalysisState with qna_results and chromadb_insert_status.
    """
    print("[NODE]: run_data_retrieval_storage")
    if not state.question_list:
        state.error_message = "No questions generated."
        return state

    messages = [
        SystemMessage(content="Fetch search results and store in vector DB."),
        HumanMessage(content=f"Questions: {json.dumps(state.question_list)}")
    ]

    response = data_retrieval_storage_agent.invoke({"messages": messages})

    # Search backwards for fetch_search_results tool output (JSON list)
    qna_results = None
    chromadb_status = None

    for msg in reversed(response["messages"]):
        content = msg.content if hasattr(msg, "content") else ""

        # Skip empty or plain-text summary messages
        if not content or not content.strip().startswith(("{", "[")):
            continue

        try:
            parsed = json.loads(content.strip())

            # etch_search_results returns a list → qna_results
            if isinstance(parsed, list) and qna_results is None:
                qna_results = parsed
                print(f"[STATE] QnA Results: {len(qna_results)} entries parsed")

            # store_in_chromadb returns a dict with chromadb_insert_status
            elif isinstance(parsed, dict) and "chromadb_insert_status" in parsed:
                chromadb_status = parsed.get("chromadb_insert_status", False)
                print(f"[STATE] ChromaDB Status: {chromadb_status} (from tool output)")

        except json.JSONDecodeError:
            continue

        # Stop once both values are found
        if qna_results is not None and chromadb_status is not None:
            break

    # pdate state with extracted values or safe defaults
    if qna_results is not None:
        state.qna_results = qna_results
    else:
        print("[WARNING]: Could not extract QnA results, defaulting to []")
        state.qna_results   = []
        state.error_message = "Failed to parse QnA results from agent response."

    state.chromadb_insert_status = chromadb_status if chromadb_status is not None else False

    if chromadb_status is None:
        print("[WARNING]: Could not extract chromadb_insert_status, defaulting to False")

    return state

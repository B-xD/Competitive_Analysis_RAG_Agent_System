# run_question_generator node
from ..state import CompetitiveAnalysisState
from langchain_core.messages import HumanMessage, SystemMessage
from ..agents import question_generator_agent
import json 
from ..config import tictoc

def run_question_generator(state: CompetitiveAnalysisState) -> CompetitiveAnalysisState:
    """
    Invoke the question-generation agent
    produce structured JSON output
    parses that output to update the pipeline state

    Args:
        state: The current CompetitiveAnalysisState object.

    Returns:
        Updated CompetitiveAnalysisState with sector, validity flag, and question list.

    """

    print("[NODE]: run_question_generator")
    messages = [
        SystemMessage(content="Generate questions for competitive analysis."),
        HumanMessage(content=f"Company: {state.company_name}, Max questions: {state.max_num_of_questions}")
    ]
    try:
        response = question_generator_agent.invoke({"messages": messages})

        # Find the last message with valid JSON content
        last_message = None
        for msg in reversed(response["messages"]):
            if hasattr(msg, 'content') and isinstance(msg.content, str) and msg.content.strip().startswith('{'):
                last_message = msg.content
                break
        if last_message is None:
            last_message = response["messages"][-1].content if response["messages"] else ""
            print(f"[WARNING]: No valid JSON message found, using last message: {last_message}")

        try:
            output = json.loads(last_message)
            state.sector           = output.get("sector", "")
            state.is_valid_company = output.get("is_valid_company", False)
            state.question_list    = output.get("questions", [])
            state.error_message    = output.get("error_message", None)
            print(f"[PARSED OUTPUT]: sector={state.sector}, is_valid_company={state.is_valid_company}, questions={len(state.question_list)}")

        except json.JSONDecodeError as e:
            print(f"[ERROR]: Failed to parse JSON from question_generator_agent: {str(e)}")
            print(f"[RAW RESPONSE CONTENT]: {last_message}")
            state.error_message    = f"Failed to parse JSON from question_generator_agent: {str(e)}"
            state.sector           = ""
            state.is_valid_company = False
            state.question_list    = []

    except Exception as e:
        print(f"[ERROR]: Question generator agent failed: {str(e)}")
        state.error_message    = f"Question generator agent failed: {str(e)}"
        state.sector           = ""
        state.is_valid_company = False
        state.question_list    = []

    return state
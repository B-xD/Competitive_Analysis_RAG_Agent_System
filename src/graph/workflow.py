from langgraph.graph import StateGraph, START, END
from ..state import CompetitiveAnalysisState
from ..nodes import run_question_generator, run_data_retrieval_storage,  run_report_drafter

# Build the LangGraph workflow
workflow = StateGraph(CompetitiveAnalysisState)

workflow.add_node("question_generator",       run_question_generator)
workflow.add_node("data_retrieval_storage",   run_data_retrieval_storage)
workflow.add_node("report_drafter",           run_report_drafter)

workflow.add_edge(START,                    "question_generator")
workflow.add_edge("question_generator",     "data_retrieval_storage")
workflow.add_edge("data_retrieval_storage", "report_drafter")
workflow.add_edge("report_drafter",         END)

competitive_analysis = workflow.compile()
print("[GRAPH] Workflow compiled successfully.")
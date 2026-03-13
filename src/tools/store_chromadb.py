from typing import List, Dict
from ..config import MAX_NUM_OF_QUESTIONS, vector_store
import time
import json
from langchain.agents import tool

@tool
def store_in_chromadb(qna_results: List[Dict]) -> str:
    """
    Store question-answer pairs into ChromaDB vector store for later retrieval.
    Skips empty answers and tracks insertion status.

    Args:
        qna_results: A list of question-answer dictionaries with 'Question' and 'Answer' keys.

    Returns:
        A JSON-formatted string indicating the insertion status and document count.
    """
    #qna_results =json.loads(fetch_search_results(question_list))
    start_time = time.time()
    print("CREATING DOCUMENTS WITH METADATA...")

    documents = []
    metadatas = []
    ids = []
    doc_counter = 1

    for qna in qna_results:
        answer = qna.get("Answer", "").strip()
        question = qna.get("Question", "")

        if not answer:
            print(f"[SKIP] No answer for question: '{question}'")
            continue

        documents.append(answer)
        metadatas.append({
            "question": question,
            "source_type": "answer",
            "search_success": True
        })
        ids.append(f"doc_{doc_counter}")
        doc_counter += 1

    if not documents:
        return json.dumps({
            "chromadb_insert_status": False,
            "inserted_count": 0,
            "error_message": "No valid answers to store."
        })

    print("CACHING DOCUMENTS INTO CHROMADB...")
    insert_status = False

    try:
        for i in range(0, len(documents), MAX_NUM_OF_QUESTIONS):
            batch_docs = documents[i:i + MAX_NUM_OF_QUESTIONS]
            batch_meta = metadatas[i:i + MAX_NUM_OF_QUESTIONS]
            batch_ids  = ids[i:i + MAX_NUM_OF_QUESTIONS]

            vector_store.add_texts(
                texts=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            time.sleep(1)

        insert_status = True
        end_time = time.time()
        print(f"Successfully inserted {len(documents)} documents into ChromaDB.")
        print(f"Execution time: {end_time - start_time:.2f}s")

    except Exception as e:
        print(f"[ERROR] ChromaDB insertion failed: {str(e)}")
        return json.dumps({
            "chromadb_insert_status": False,
            "inserted_count": 0,
            "error_message": str(e)
        })

    return json.dumps({
        "chromadb_insert_status": insert_status,
        "inserted_count": len(documents),
        "error_message": None
    })
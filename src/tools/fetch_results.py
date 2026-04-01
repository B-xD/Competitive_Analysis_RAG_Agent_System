from ..config import tavily_search
from typing import List 
import json 
from langchain.agents import tool

@tool
def fetch_search_results(question_list: List[str]) -> str:
  """
      Retrieve answers for competitive analysis questions using the Tavily Search API.
      Iterates over each question, queries Tavily, and returns question-answer pairs.

    Args:
        question_list: A list of competitive analysis questions to search for.

    Returns:
        A JSON-formatted string containing a list of question-answer dictionaries.
     """
  #list of questions
  #question_list = json.loads(questions)['questions']
    #create
  names = ['Question', 'Answer']
  QnA_list = []

  for question in question_list:

    try:
        search_answer = tavily_search.invoke({"query": question})

        answer = search_answer.get('aswer') if search_answer.get('aswer') is not None else " "

        QnA_dict = {names[0]:search_answer['query'],names[1]: search_answer['answer']}
        QnA_list.append(QnA_dict)

    except Exception as e:
      print(f'Error:{str(e)}')
      QnA_dict = {names[0]:search_answer['query'],names[1]: ''}
      QnA_list.append(QnA_dict)

    result = json.dumps(QnA_list)

  return result
from ..config import tavily_search, llm
from ..state import QuestionSuggestion
from langchain_core.prompts import ChatPromptTemplate
import json
from langchain.agents import tool

@tool
def suggest_questions(company_name: str, max_num_of_questions: int) -> str:
  """
  Take the company name {company_name} and the maximum number os questions {max_num_of_questions} as an inpute
  generate competitive analysis questions


  """

  sytem_message = """
  You are a powerful competitive analysis questions generator.
  take the company name {company_name}, check if the company is real/recognized
  if the company name is not not recognized return is_valid_company False
  if the company exists identify the industry / sector  it operates in
  then generate targeted competitive analysis questions covering competitors, pricing, technology, supply chain, strengths, weaknesses, and market opportunities.
  store the generated questions and store them in the list called questions

  Constraints:
  Do not generate more than {max_num_of_questions} number of questions

  """

  #check is the company name exists
  #we will verify the company name in two laters: 1st throught tavily search and then through the LLM
  print("--VALIDATING COMPANY NAME FROM WEBSEARCH--")
  search_company_name = tavily_search.invoke(input= company_name+' '+'company')
  if company_name in search_company_name['results'][0]['title']:
    #state.is_valid_company == True

    print(f'Name: {company_name} is a valid company! \n')
  else:
    #state.is_valid_company == False
    print(f'Name: {company_name} is not a valid company! \n')

  try:
      prompt = ChatPromptTemplate.from_messages([
          ('system', sytem_message),
          ('user', f'company: {company_name}. Generate up to {max_num_of_questions} questions')
      ])

      chain = prompt | llm.with_structured_output(QuestionSuggestion)
      result = chain.invoke({
          'company_name': company_name,
          'max_num_of_questions': max_num_of_questions
      })


      print("--VALIDATING COMPANY NAME FROM LLM--")
      is_valid_company = result.is_valid_company
      print(f'Is {company_name} a valid company? {is_valid_company} \n')

      print(f'---RETRIEVING {company_name.upper()} INDUSTRY--')
      sector = result.sector
      print(f'Sector: {sector} \n')

      print('----GETTING LIST OF QUESTIONS--')
      questions = result.questions
      n = 1
      for question in questions :
        print(f'Question {n}: {question}')
        n+=1

      print(f'\n--COMPETITIVE ANALYSIS QUESTIONS GENERATED SUCCESSFULLY FOR {company_name.upper()}-- \n')

      output = {
          'sector': sector,
          'is_valid_company': is_valid_company,
          'questions': questions,
          'error_message': result.error_message

      }


  except Exception as e:
      print(f'An error as occurred: {str(e)}')

      output = {
          'sector': '',
          'is_valid_company': False,
          'questions': [],
          'error_message': str(e)

      }


  return json.dumps(output)
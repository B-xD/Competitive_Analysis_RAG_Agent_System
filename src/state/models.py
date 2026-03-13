from pydantic import BaseModel, Field
from typing import TypedDict, Optional, List, Dict, Tuple, Any  
from ..config import MAX_NUM_OF_QUESTIONS



# Define the QuestionSuggestion Pydantic model
class QuestionSuggestion(BaseModel):
  """
  The structured output for the competitive analysis
  """
  sector: str = Field(None, description= 'The industry sector of the company.')
  is_valid_company: bool = Field(default = False, description='A boolean flag for whether the company name is recognized/ exists, if not returns Unkown')
  questions: List[str] = Field(default=[], desctiption = 'a list of the actual reasearch questions to be answered')
  error_message: str = Field(None, description='Optional field to capture any errors that occur')

# Define CompetitiveAnalysisState Pydantic model
class CompetitiveAnalysisState(BaseModel):

  company_name: str = Field(None, description= 'The company being analyzed')
  max_num_of_questions: int = Field(default = MAX_NUM_OF_QUESTIONS, description='The maximum number of questions to generate')
  sector: Optional[str] = Field(None, description='The industry sector')

  is_valid_company: Optional[bool] = Field(default = False, description='Boolean flag to mark if the company is recognized ')

  question_list: Optional[List[str]] = Field(None, description='List of generated analysis questions ')

  qna_results: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of question-answer pairs generated during analysis"
    )
  vectorstore: Optional[Any] = Field(default = None, description='Chroma vector database instance for retrieval')
  chromadb_insert_status: Optional[bool] = Field(default = False, description='Tracks whether data was successfully stored in Chroma')
  report: Optional[str] = Field(default= None, description = 'Final competitive analysis report')
  error_message: Optional[str] = Field(default = None, description='Captures any error details ')

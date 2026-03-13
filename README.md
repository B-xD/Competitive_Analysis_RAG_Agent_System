# Competitive Analysis RAG System

Multi-Agent Retrieval-Augmented Generation system for automated competitor analysis.

## Architecture
START → Question Generation → Data Retrieval/Storage → Report Drafting → END

## Setup
1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Run the notebook or execute directly:

## Usage
\```python
from src.graph.workflow import competitive_analysis
from src.state.models import CompetitiveAnalysisState

result = competitive_analysis.invoke(
    CompetitiveAnalysisState(company_name="Tesla", vectorstore=vector_store)
)
print(result["report"])
\```

## Project Structure
...

## Agents
- **Question Generator** — validates company, identifies sector, generates questions
- **Data Retrieval & Storage** — fetches answers via Tavily, stores in ChromaDB
- **Report Drafter** — retrieves context via RAG, generates structured report
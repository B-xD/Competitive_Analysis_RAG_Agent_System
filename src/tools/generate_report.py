from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import tool

@tool
def generate_report(company_name: str, sector: str) -> str:
  """
  Define how to use retrieved context for generating the report
  use the retrieved context as the primary source and comparing competitors across dimensions
  highlight differentiators and actionable strategies.
  structure the final output into the named sections and citing context where relevant

  Args:
        company_name: The name of the company being analyzed.
        sector: The industry or sector the company operates in.

  Returns:
        A ChatPromptTemplate ready for downstream RAG invocation.


  """

  system_message = """
    You are an expert competitive intelligence analyst specializing in the {sector} industry.
    Using ONLY the retrieved context provided, generate a comprehensive competitive analysis report.

    Your analysis must compare competitors across the following dimensions:
    - Market Share        : Relative positioning and growth trends
    - Products & Services : Key offerings, differentiators, and portfolio breadth
    - Pricing Strategies  : Pricing models, tiers, and value propositions
    - Technology          : Innovation, R&D investment, and tech stack advantages
    - Supply Chain        : Operational efficiency, sourcing, and logistics strengths
    - Customer Sentiment  : Brand perception, reviews, loyalty, and satisfaction

    Additionally, your report must:
    - Highlight key differentiators that set {company_name} apart from competitors
    - Identify potential threats and vulnerabilities
    - Propose clear, actionable strategies for {company_name} to strengthen its market position

    Structure your report using the following sections:
    1. Executive Summary
    2. Industry Overview
    3. Competitor Landscape
    4. Dimension-by-Dimension Comparison
    5. Key Differentiators
    6. Threats & Vulnerabilities
    7. Actionable Recommendations
    8. Conclusion

    Cite the retrieved context where relevant to support your findings.
    If the context does not contain sufficient information for a section, state that explicitly.
    """

  human_message = """
    Generate a full competitive analysis report for **{company_name}** operating in the **{sector}** sector.

    Use the following retrieved context as your primary source of information:

    {context}

    Ensure the report is structured, evidence-based, and concludes with actionable strategies.
    """

  prompt = ChatPromptTemplate.from_messages([
      ("system", system_message),
      ('human', human_message)
  ])

  return prompt

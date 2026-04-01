from src import competitive_analysis, CompetitiveAnalysisState,vector_store 
from IPython.display import Image, display, Markdown

#define endpoint 
companyname = str(input('Enter company name:')).strip()

result =competitive_analysis.invoke(
    CompetitiveAnalysisState(
        company_name = companyname,
        vectorstore=vector_store
        )
    )

print("FINAL REPORT")
print(result['report'])

#save the grapth into output 
try:
    display(Image(competitive_analysis.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    print(f"[VISUALIZATION] Could not render graph image: {str(e)}")
    print(competitive_analysis.get_graph().draw_mermaid())
    pass


display(Markdown(result['report']))

with open(f'outputs/{companyname}_competive_analysis.md', 'w') as f:
    f.write(result['report'])

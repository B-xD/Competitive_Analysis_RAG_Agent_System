from src import competitive_analysis, CompetitiveAnalysisState,vector_store 

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



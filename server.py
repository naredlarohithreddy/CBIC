import os
import pandas as pd
import sqlite3
import re 
from langchain_ibm import WatsonxLLM
from pathlib import Path
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import asyncio
import subprocess
import sys

def executing_data_files(files_path):
    result=subprocess.run([sys.executable,files_path],capture_output=True,text=True)

    if result.returncode == 0:
        return {"message": f"Script executed successfully: {files_path}", "output": result.stdout}
    else:
        return {"message": f"Error executing script: {files_path}", "error": result.stderr}

def execute_all_files(folder_path):
    # python_files = [file for file in os.listdir(folder_path) if file.endswith('.py')]

    results=[]

    fixed_order=[
        'taxpayer_info.py',
        'taxpayer_registration.py',
        'tax_filings.py',
        'tax_payments.py',
        'tax_invoices.py',
        'tax_refunds.py',
        'appeals_and_disputes.py'
    ]

    python_files = [file for file in fixed_order if file in os.listdir(folder_path)]

    for file in python_files:
        script_path=os.path.join(folder_path,file)
        result=executing_data_files(script_path)
        results.append(result)
    
    return results

def get_credentials():
    os.environ["WATSONX_APIKEY"] = os.getenv('WATSONX_API_KEY')
    os.environ["WATSONX_URL"] = os.getenv('WATSONX_URL')

    project_id = os.getenv('PROJECT_ID')
    return project_id

def create_agents():
    project_id = get_credentials()

    parameters_1 = {
        "decoding_method": "sample",
        "max_new_tokens": 4000,
        "top_k": 50,
        "top_p": 1,
        "repetition_penalty": 1.0,
        "temperature": 0.5 
    }

    parameters_2 = {
        "decoding_method": 'greedy',
        "max_new_tokens": 4000,
        "min_new_tokens": 5,
        "temperature": 0,
        "repetition_penalty":1.0
    }

    sql_model_id = 'mistralai/mistral-large' #meta-llama/llama-3-70b-instruct
    reviewer_model_id = 'mistralai/mistral-large' #mistralai/mistral-large
    
    sql_llm = WatsonxLLM(
        model_id = sql_model_id,
        project_id = project_id,
        params = parameters_1
    )

    reviewer_llm = WatsonxLLM(
        model_id = reviewer_model_id,
        project_id=project_id,
        params=parameters_2
    )

    return sql_llm, reviewer_llm

def get_files_of_type(folder_path, file_extension):
    folder = Path(folder_path)
    return list(folder.glob(f'*{file_extension}'))

def create_SQL_database(folder_path, database_name):
    file_extension = '.csv' 
    files = get_files_of_type(folder_path,file_extension)

    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    for file_name in files:
        df = pd.read_csv(file_name,sep='|')
        df.columns = df.columns.str.replace(' ', '_')
        df.to_sql(file_name.stem, conn, if_exists='replace', index=False)
        print(f"Uploaded sheet '{file_name}' as table '{file_name.stem}'")
        
    conn.commit()
    c.close()
    print("All sheets uploaded")

def execute_SQL_query(query):
    conn = sqlite3.connect('cbic.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    
    result=[]
    for row in rows:
      result.append(row)
    c.close()
    return result

def get_table_description(data_file_path,file_extension):

    files=get_files_of_type(data_file_path,file_extension)

    table_description=[]
    for file in files:

        df = pd.read_csv(file,sep='|')
        table_desc =  "\nTable Name : " + file.stem
        df.columns = df.columns.str.replace(' ', '_')
        i=0
        p='primary key'
        for name in df.columns:
            if i==0:
                table_desc += "\nTable column Description : " + name + " \n which is " + p + " and data type of column is " + str(type(df[name][0])) +  " \nexample for the column" + ' are  ' + str(df[name][0]) + ', ' + str(df[name][1]) + ', '+ str(df[name][2])    
                i=1
            else:
                table_desc += "\nTable column Description : " + name + " \n and data type of column is " + str(type(df[name][0])) +  " \nexample for the column" + ' are  ' + str(df[name][0]) + ', ' + str(df[name][1]) + ', '+ str(df[name][2])
        
        table_description.append(table_desc)
        
    return table_description

def generate_SQL_query(table_description, user_input, sql_llm):

    """Generates SQL query"""

    prefix_sql=f'''As an expert SQL query writer specializing in SQLite, your goal is to craft efficient, optimized SQL queries tailored to user needs. Your queries should seamlessly interact with SQLite databases, making use of appropriate type casting to float when calculating percentages. Avoid using multiple JOIN statements directly in the main query. Instead, use Common Table Expressions (CTEs) or subqueries to simplify complex join logic and enhance readability. Note that SQLite does not support RIGHT JOIN or OUTER JOIN.

    Use appropriate column names from the tables provided in the table_description.
    Use type casting to float when calculating percentages.Use standard date formats when representing quarters, fiscal years, or time periods.

    Output Requirements: Based on user queries, the output should and Avoid directly referencing columns that are not present in the selected table unless the query requires a join with another table (in which case, use a subquery or a Common Table Expression (CTE)):
   - Group by non-primary key columns (e.g., regions or states) when requested.Exclude unnecessary identifiers (e.g., taxpayer IDs) unless explicitly asked to include them.

    If the user asks about the fiscal year, include all quarters in that year.If the user asks about a specific quarter, include only data from that one quarter.When referring to quarters or years, always use the standard date format.

    Example structure for queries involving aggregated metrics:
    
    when representing quarter or year, always use standard date format instead of natural language
    when user_input asks about fiscal year then consider all quarters in a year and when user_input asks about quarter then only include one quarter
    ALWAYS USE COALESCE WHILE AGGREGATING THE VALUES and better at handling null values.
    
    example1:

    WITH EntityAggregates AS (
        SELECT
            EntityID,
            SUM(Value) AS TotalValue
        FROM
            EntityTable
        GROUP BY
            groupcolumn
    ),
    TargetAggregates AS (
        SELECT
            EntityID,
            SUM(Target) AS TotalTarget
        FROM
            TargetTable
        WHERE
            TimePeriod = 'SpecificPeriod'
        GROUP BY
            groupcolumn
    )
    SELECT
        E.EntityID,
        E.EntityName,
        COALESCE(EA.TotalValue, 0) AS TotalValue,
        COALESCE(TA.TotalTarget, 0) AS TotalTarget,
        ROUND((COALESCE(EA.TotalValue, 0) / CAST(COALESCE(TA.TotalTarget, 0) AS FLOAT)) * 100, 2) AS PercentageAchievement
    FROM
        EntityDetails E
    LEFT JOIN
        EntityAggregates EA ON E.EntityID = EA.EntityID
    LEFT JOIN
        TargetAggregates TA ON E.EntityID = TA.EntityID
    ORDER BY
        PercentageAchievement DESC;

    example2:

    
    Template for Handling Specific Grouping by Columns:
        
        WITH EntityAggregates AS (
        SELECT
            EntityID,
            SUM(Value) AS TotalValue
        FROM
            EntityTable
        GROUP BY
            groupcolumn
    )
    SELECT
        E.EntityID,
        E.EntityName,
        COALESCE(EA.TotalValue, 0) AS TotalValue
    FROM
        EntityDetails E
    LEFT JOIN
        EntityAggregates EA ON E.EntityID = EA.EntityID
    GROUP BY
        E.EntityName
    ORDER BY
        TotalValue DESC;

    Ensure that you use the column names exactly as provided in the information. Output the SQL query as a string.
    YOUR RESPONSE MUST CONTAIN ONLY THE SQL QUERY.
    
    Avoid using SQL reserved keywords as aliases.
    Ensure that the aliases used for tables and columns do not conflict with SQL reserved keywords.
    Example of SQL reserved keywords: SELECT, FROM, WHERE, JOIN, AS, ON, AND, OR, NOT, IN, EXISTS, IS, NULL, LIKE, BETWEEN, UNION, INTERSECT, MINUS, DISTINCT, ORDER, BY, GROUP, HAVING, LIMIT, OFFSET, ALL, ANY, SOME, INTO, CASE, WHEN, THEN, ELSE, END, CAST, CONVERT, TO, WITH.

    Generate the SQL query based on the above requirements.

    ONLY ONE SQL QUERY as a string. 
    
    Question : {user_input}
    Table Description which consists of table columns their data types and sample entries: {table_description}
    SQL Query :'''
    

    sql_response = sql_llm.invoke(prefix_sql).strip()
    pattern = re.compile(r'SQL_QUERY\s*=\s*"""\s*(.*?)\s*"""', re.DOTALL)

    match = pattern.search(sql_response)

    if match:
        sql_response = match.group(1)
    sql_response = sql_response.replace('```sql', '').replace('```', '').strip()
    print(sql_response)
    return sql_response

def validate_SQL_query(table_description, user_input, query, reviewer_llm):
    
    prefix_validation = f""" As a professional SQL specialist, you have been assisting users with refining their SQL queries for various projects and tasks. Your ability to identify and correct syntax errors, optimize query performance, and ensure logical accuracy has earned you a stellar reputation in the industry.
    Your task today is to review and rewrite a SQL query for a user. The user will provide you with their initial query and any specific requirements they have. It is crucial that you pay attention to details, adhere to best practices, and enhance the query's efficiency while maintaining its intended functionality.
        
    Important Points to Consider:
    1. Verify the SQL query is based solely on the provided information.
    2. Do not make assumptions beyond the provided details, especially regarding IDs.
    3. Sample rows are for context only and should not be used as actual data.
    4. If the query involves finding an ID based on a name, first extract the ID from the appropriate table.
    5. Optimize the query and ensure proper use of indexes.
    6. Ensure compliance with SQLite rules, especially when working with date functions (use `strftime` instead of `MONTH()`).
    7. Type cast to float when calculating percentages.
    8. Ensure all columns used belong to their respective tables.
    9. Avoid using RIGHT JOIN or OUTER JOIN as they are not supported by SQLite.
    10. For complex join logic, consider using Common Table Expressions (CTEs) to break down the query.
    11. If the query involves more than two JOIN statements, provide a different approach using subqueries, CTEs, or breaking down the query into smaller parts.
    12. Use group by if it is necessary.
    13. Use appropriate column names from the tables provided in the table_description.
    14. Use type casting to float when calculating percentages.Use standard date formats when representing quarters, fiscal years, or time periods.
    15. Avoid directly referencing columns that are not present in the selected table unless the query requires a join with another table (in which case, use a subquery or a Common Table Expression (CTE)).

     Example for complex joins:
        Original:
        SELECT A.Col1, B.Col2, C.Col3 
        FROM TableA A 
        JOIN TableB B ON A.ID = B.A_ID 
        JOIN TableC C ON B.ID = C.B_ID 
        WHERE A.Condition = 'Value';

        Revised using CTEs:
        WITH CTE1 AS (
            SELECT A.ID, A.Col1 
            FROM TableA A 
            WHERE A.Condition = 'Value'
        ),
        CTE2 AS (
            SELECT B.A_ID, B.Col2 
            FROM TableB B 
            JOIN CTE1 ON CTE1.ID = B.A_ID
        )
        SELECT CTE1.Col1, CTE2.Col2, C.Col3 
        FROM TableC C 
        JOIN CTE2 ON CTE2.B_ID = C.B_ID;
    
    Avoid using SQL reserved keywords as aliases.
    Ensure that the aliases used for tables and columns do not conflict with SQL reserved keywords.
    Example of SQL reserved keywords: SELECT, FROM, WHERE, JOIN, AS, ON, AND, OR, NOT, IN, EXISTS, IS, NULL, LIKE, BETWEEN, UNION, INTERSECT, MINUS, DISTINCT, ORDER, BY, GROUP, HAVING, LIMIT, OFFSET, ALL, ANY, SOME, INTO, CASE, WHEN, THEN, ELSE, END, CAST, CONVERT, TO, WITH.

    Generate the SQL query based on the above requirements.

    The query is correct only if it satisfies all these conditions. If it is not correct, provide the corrected SQL query.

    Output only the SQL query. Do not provide any explanation.

    
    Only if the query satisfies all these conditions it is correct.
    Is the SQL query correct? If not, please provide the correct SQL query.
    Output the SQL query. Even the Given Query is Correct output the same query.
    Do not provide any explanation. Only the query.
    ONLY OUTPUT THE SINGLE CORRECT QUERY.

    Question: {user_input}
    Table Description: {table_description}
    SQL Query: {query}

    Corrected SQL Query: """
    reviewer_response = reviewer_llm.invoke(prefix_validation)
    validated_query = re.sub(r'"""', '', reviewer_response)
    validated_query = validated_query.replace('```sql', '').replace('```', '').strip()
    validated_query = validated_query.split(';')[0] + ';'
    print(validated_query)
    return validated_query

def create_visualization(database_name, user_input, query, graph_llm, html_file):

    prompt = f'''Generate a chart compulsarily on the given data.You are tasked with generating a variety of data visualizations that effectively communicate insights from complex datasets. The visualizations should go beyond just bar charts and tables, incorporating different types of charts like pie charts, scatter plots, line plots, area plots, heatmaps, bubble plots, and radar plots based on the results of a SQL query.
    select the type of chart based on the data, do check keenly and generate the chart.
    Do not use same color theme for representing each and every type of data. 
    the legends must be visible in the graph, it shouldn't be blacked out in graph.

    Input Question: {user_input}
    SQL Query: {query}

    For each visualization, you must:

    Handle Missing Data (None Values): Ensure that missing values are excluded from the visualizations, meaning they should not appear on any chart.
    Don't ignore negative value results, plot them also.
    Effective Value Scaling: For data where there is a significant discrepancy between values (e.g., large positive values versus small or negative ones), adjust the scaling so that all values are visible and meaningful. Use appropriate axis scaling (e.g., log scale, min-max scaling, or normalization) to give impact to smaller values while maintaining the relevance of larger ones.
    Use Plotly Express to generate the chart visuals.
    Ensure the chart or table is clear, concise, and visually appealing, providing meaningful insights into the data extracted from the SQL query.
    Apply appropriate labels, titles, and formatting to enhance the presentation.
    The query must be stored in a variable. The code should be ready for execution with no placeholders requiring manual input
    The data will be extracted from a database stored in the {database_name} file located in the same parent folder.
    Save the generated visualization as {html_file}.ensure the chart corresponds to the actual structure of the dataset.
    Output only the code as a string without explanations. Ensure proper indentation for code blocks under if else statements.
    NOTE: Do not use unnecessary indents or backticks.
    '''

    
    code_response = graph_llm.invoke(prompt).strip()

    lines = code_response.split('\n')
    lines = [line for line in lines[1:-1]]
    code_response = '\n'.join(lines)
    pattern = r'```python'
    cleaned_code = re.sub(pattern, '', code_response, flags=re.IGNORECASE)
    print(cleaned_code)
    try:
        exec(cleaned_code,locals())
    except Exception as e:
        print("Error in generating chart. The error was ", e)

def generate_response(reviewer_llm, user_input, result):
    prompt = f"""
        Given the user question, table description and the results of runnning an SQL query, 
        generate an appropriate natural language response based on the results and user question.
        Return only the response which is comprehendable by the user. Do not provide unnecessary details such as table and column description.
        Return the response in bullet points.

        Question : {user_input}
        Results: {result}
        Response:
    """
    NL_response = reviewer_llm.invoke(prompt).strip()
    
    pattern = r'^Response:\s*(.*)'

    match = re.search(pattern, NL_response)
    if match:
        extracted_text = match.group(1)
        NL_response = extracted_text
    return NL_response

def generate_pipeline(sql_llm, reviewer_llm, user_input, database_name, table_description, html_file=None):
    print("Generating SQL query...")
    query = generate_SQL_query(table_description, user_input, sql_llm)
    print("Validating SQL query...")
    valid_query = validate_SQL_query(table_description, user_input, query, sql_llm)

    answer = execute_SQL_query(valid_query)
    result = str(answer)

    if html_file:
        print("Generating visualizations")
        create_visualization(database_name, user_input, valid_query, sql_llm, html_file)

    final_response = generate_response(reviewer_llm, user_input, result)
    print(final_response)

    return final_response


class Userinput(BaseModel):
    question: str

class Stateinput(BaseModel):
    state: str

app = FastAPI(openapi_version="3.0.3")

@app.post("/generate/chatbot")
async def generate1(input: Userinput):
    user_input = input.question
    
    HTML_FILE_INDUSTRY = f"./newcharts/contributingind.html"
    result = await asyncio.to_thread(generate_pipeline, sql_llm, reviewer_llm, user_input, database_name, table_description, HTML_FILE_INDUSTRY)
    
    return result

@app.post("/generate/state")
async def generate2(input: Stateinput):
    user_input = input.state
    
    HTML_FILE_QUARTER = f"./newcharts/question1.html"  
    q1 = f'what are the top five industries contributing to the revenue in {user_input}'
    result = await asyncio.to_thread(generate_pipeline, sql_llm, reviewer_llm, q1, database_name, table_description, HTML_FILE_QUARTER)
    
    return result

@app.post("/generate/dispute")
async def generate3(input: Stateinput):
    user_input = input.state
    
    HTML_FILE_DISPUTE = f"./newcharts/dispute.html"
    q1 = f'count of different disputes types in {user_input}'
    result = await asyncio.to_thread(generate_pipeline, sql_llm, reviewer_llm, q1, database_name, table_description, HTML_FILE_DISPUTE)
    
    return result

if __name__ == '__main__':
    data_file_path='./v4'
    results=execute_all_files(data_file_path)

    database_name = "cbic.db"
    create_SQL_database(data_file_path, database_name)

    sql_llm, reviewer_llm = create_agents()
    table_description = get_table_description(data_file_path,file_extension='.csv')

    uvicorn.run(app, host="127.0.0.1", port=8000)
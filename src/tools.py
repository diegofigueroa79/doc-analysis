import textractcaller as tc
from textractor.parsers import response_parser
from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate
import pandas as pd
import numpy as np
import boto3
import os
import re



QUERY_1 = "Choose from the three types to answer the question: balance sheet, income, cash flow. What type is the document?"
QUERY_2 = "What is the company name?"
QUERY_3 = "What is the month or date or year ended?"

def extract_document(file_path):
    textract = boto3.client('textract', region_name='us-east-1')
    q = tc.Query(text=QUERY_1, pages=["*"])
    q2 = tc.Query(text=QUERY_2, pages=["*"])
    q3 = tc.Query(text=QUERY_3, pages=["*"])
    
    result = tc.call_textract(
        input_document=file_path,
        queries_config=tc.QueriesConfig(queries=[q,q2,q3]),
        adapters_config=None,
        features=[tc.Textract_Features.QUERIES, tc.Textract_Features.TABLES, tc.Textract_Features.LAYOUT],
        force_async_api=True,
        boto3_textract_client=textract
    )
    
    document = response_parser.parse(result)
    return document

def build_tables_dict(llm, document):
    doc_tables = {}
    financial_quarter = get_financial_quarter(llm, str([q.result for q in document.queries if q.query == QUERY_3][0]))
    
    for page in document.pages:
        # what is the doc type and company name?
        company_name = str([q.result for q in page.queries if q.query == QUERY_2][0])
        if company_name not in doc_tables.keys():
            doc_tables[company_name] = {}
        doc_type = str([q.result for q in page.queries if q.query == QUERY_1][0])
        if doc_type not in doc_tables.keys():
            doc_tables[company_name][doc_type] = []
        # extract tables
        for table in page.tables:
            doc_tables[company_name][doc_type].append(table.to_pandas())

    return doc_tables, financial_quarter

def get_financial_quarter(llm, date):
    # get prompt
    template_text=open('prompt-financial-quarter.txt',"r").read()
    template = PromptTemplate.from_template(template_text)
    # format prompt with table and schema
    prompt = template.invoke(input={'date': date})
    # call llm
    response = llm.invoke(prompt)
    content = extract_output_text(response.content)
    return content

def extract_output_text(input_text):
    # Use regular expression to find text between <output> and </output> tags
    pattern = r"<output>(.*?)<\/output>"
    match = re.search(pattern, input_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return None

def parse_tuples(input_string):
    input_string = input_string.strip().split('\n')
    result = []
    for i in input_string:
        i = i.strip('(),').split('"')
        result.append([d for d in i if d != ',' and d != ''])
    return result

def generate_sql(llm, pd_table, db_path, company_name, financial_quarter):
    # get prompt
    template_text=open('prompt-sql.txt',"r").read()
    template = PromptTemplate.from_template(template_text)
    # get schema
    df = pd.read_csv(db_path, sep=',')
    schema = df.iloc[:, 0].values
    # format prompt with table and schema
    prompt = template.invoke(input={'content': pd_table, 'schema': schema, 'company_name': company_name, 'financial_quarter': financial_quarter})
    # call llm
    response = llm.invoke(prompt)
    content = extract_output_text(response.content)
    sql_tuples_list = parse_tuples(content)
    return sql_tuples_list

def database_retrieval(tuples_list, extracted_data, db_path):
    database = pd.read_csv(db_path, sep=',', index_col=0)
    final_df = pd.DataFrame(columns=np.arange(5))
    for item in tuples_list:
        extracted_vals = extracted_data.loc[item[0]].values.flatten().tolist()
        db_vals = database.loc[item[1]].values.flatten().tolist()
        final_df.loc[len(final_df.index)] = item[0] + extracted_vals
        final_df.loc[len(final_df.index)] = item[1] + db_vals
    return final_df

def connect_to_bedrock():
    boto_session = boto3.Session()
    bedrock_runtime = boto_session.client("bedrock-runtime", region_name='us-east-1')

    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    llm = ChatBedrock(model_id=modelId, client=bedrock_runtime, model_kwargs={"temperature": 0,"top_k":250,"max_tokens":3000})
    return llm
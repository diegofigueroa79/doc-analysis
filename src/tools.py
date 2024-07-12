import textractcaller as tc
from textractor.parsers import response_parser
from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import boto3
import os
import re


QUERY_1 = "Choose from the three types to answer the question: balance sheet, income, cash flow. What type is the document?"
QUERY_2 = "What is the company name?"
QUERY_3 = "What is the month or date or year ended?"

def extract_document():
    textract = boto3.client('textract', region_name='<region>')
    q = tc.Query(text=QUERY_1, pages=["*"])
    q2 = tc.Query(text=QUERY_2, pages=["*"])
    q3 = tc.Query(text=QUERY_3, pages=["*"])
    adapter = tc.Adapter(adapter_id=os.getenv("TEXTRACT_ADAPTER_ID"), version="1", pages=["*"])
    
    result = tc.call_textract(
        input_document=f"{os.getenv('S3_BUCKET_URL')}balance-sheet-1.pdf",
        queries_config=tc.QueriesConfig(queries=[q,q2,q3]),
        adapters_config=tc.AdaptersConfig(adapters=[adapter]),
        features=[tc.Textract_Features.QUERIES, tc.Textract_Features.TABLES, tc.Textract_Features.LAYOUT],
        force_async_api=True,
        boto3_textract_client=textract
    )
    
    document = response_parser.parse(result)
    return document

def build_tables_dict(document):
    doc_tables = {}
    financial_quarter = get_financial_quarter([q.result for q in document.queries if q.query == QUERY_3][0])
    
    for page in document.pages:
        # what is the doc type and company name?
        company_name = [q.result for q in document.queries if q.query == QUERY_2][0]
        if company_name not in doc_tables.keys():
            doc_tables[company_name] = {}
            doc_tables['financial_quarter'] = financial_quarter
        doc_type = [q.result for q in document.queries if q.query == QUERY_1][0]
        if doc_type not in doc_tables.keys():
            doc_tables[company_name][doc_type] = []
        # extract tables
        for table in page.tables:
            doc_tables[company_name][doc_type].append(table.to_pandas())

    return doc_tables

def get_financial_quarter(llm, date):
    # get prompt
    template_text=open('prompt-financial-quarter.txt',"r").read()
    template = PromptTemplate.from_template(template_text)
    # format prompt with table and schema
    template.invoke(input={'date': date})
    # call llm
    response = llm.invoke(template)
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
    input_string.replace('"', '')
    # Remove leading/trailing whitespace and split by newline
    lines = input_string.strip().split('\n')
    # Parse each line as a tuple
    result = [tuple(line.strip('()').split(', ')) for line in lines]
    return result

def generate_sql(llm, pd_table, db_schema, company_name, financial_quarter):
    # get prompt
    template_text=open('prompt-sql.txt',"r").read()
    template = PromptTemplate.from_template(template_text)
    # format prompt with table and schema
    template.invoke(input={'content': pd_table, 'company_name': company_name, 'financial_quarter': financial_quarter})
    # call llm
    response = llm.invoke(template)
    content = extract_output_text(response.content)
    sql_tuples_list = parse_tuples(content)
    return sql_tuples_list

def connect_to_bedrock():
    boto_session = boto3.Session()
    bedrock_runtime = boto_session.client("bedrock-runtime", region_name="us-east-1")

    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    llm = ChatBedrock(model_id=modelId, client=bedrock_runtime, model_kwargs={"temperature": 0,"top_k":250,"max_tokens":3000})
    return llm


if __name__ == '__main__':
    load_dotenv()
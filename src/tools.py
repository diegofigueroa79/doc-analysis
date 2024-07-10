import textractcaller as tc
from textractor.parsers import response_parser
from langchain_aws import ChatBedrock
import boto3


def extract_document():
    document = None
    return document

def build_tables_dict(document):
    doc_tables = {}
    
    for page in document.pages:
        # what is the doc type and company name?
        company_name = page.queries[1].result
        if company_name not in doc_tables.keys():
            doc_tables[company_name] = {}
        doc_type = page.queries[0].result
        if doc_type not in doc_tables.keys():
            doc_tables[company_name][doc_type] = []
        # extract tables
        for table in page.tables:
            doc_tables[company_name][doc_type].append(table.to_pandas())

    return doc_tables

def generate_sql(llm, pd_table, db_schema):
    # get prompt
    # format prompt with table and schema
    # call llm
    sql_tuples_list = []
    return sql_tuples_list

def connect_to_bedrock():
    boto_session = boto3.Session()
    bedrock_runtime = boto_session.client("bedrock-runtime", region_name="us-east-1")

    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    llm = ChatBedrock(model_id=modelId, client=bedrock_runtime, model_kwargs={"temperature": 0,"top_k":250,"max_tokens":3000})
    return llm
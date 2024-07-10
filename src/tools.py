import textractcaller as tc
from textractor.parsers import response_parser
from langchain_aws import ChatBedrock
import boto3


def extract_document():
    textract = boto3.client('textract', region_name='<region>')
    q = tc.Query(text="Choose from the three types to answer the question: balance sheet, income, cash flow. What type is the document?", pages=["1", "2", "3"])
    q2 = tc.Query(text="What is the company name?", pages=["1", "2", "3"])
    adapter = tc.Adapter(adapter_id="<textract adapter id>", version="1", pages=["1", "2", "3"])
    
    result = tc.call_textract(
        input_document="<bucket>combined-statements.pdf",
        queries_config=tc.QueriesConfig(queries=[q,q2]),
        adapters_config=tc.AdaptersConfig(adapters=[adapter]),
        features=[tc.Textract_Features.QUERIES, tc.Textract_Features.TABLES, tc.Textract_Features.LAYOUT],
        force_async_api=True,
        boto3_textract_client=textract
    )
    
    document = response_parser.parse(result)
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

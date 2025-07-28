# math_server.py
import json

from mcp.server.fastmcp import FastMCP
import psycopg2 as psdb
from langchain_community.document_loaders import WebBaseLoader

from langchain_community.document_loaders import PyMuPDFLoader

import datetime

mcp = FastMCP("Math")

db_params = {"host":"localhost", "user":"bhargav", "password":'Bhargav@264', 'port':5432, "database":"stocks_data"}

class DatabaseConn(object):
    def __init__(self, **kwargs):
        self.params = kwargs.get("params")

    def __enter__(self):
        self.conn = psdb.connect(**self.params)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self,*args):
        self.cursor.close()
        self.conn.close()

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool(description="This tool helps to generate table schema")
def generate_schema(table_name:str):
    """
    This helps to generate table schema based on table_name

    Args: table_name

    Return: List of tuple with column names and data_type

    """
    q = """  
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = %s;

    """
    with DatabaseConn(params=db_params) as db:
        db.execute(q, (table_name,))
        db_schema = db.fetchall()

    return db_schema

@mcp.tool(name="FetchStocksDetails", description="This tool helps to fetch symbols")
def fetch_symbols():
    """
       This tool helps read the json file for understanding the symbols and stock_name having my database.
       It will help  to better understand of symbols and stock_name before creation of query it contains dict
       of symbol and stock_name.

       *** if user enter some stock name then consider final_data as a dict not file data. ***

       Example of final data : {"symbol":"stock_name"}

       Return : None

       """
    path = "/opt/MCP_Demo/symbols.json"
    with open(path, 'r') as json_file:
        symbols_data = json.load(json_file)
    final_data = {}
    for symbol,stock_name in symbols_data.items():
        symbol = symbol[4:-3]
        final_data[symbol] = stock_name
    return final_data

@mcp.tool(description="This tool apply select query on table")
def process_query(query:str):
    """
    This tools helps to provide data to user query

    Args : query

    Return : List of tuple

    """
    with DatabaseConn(params=db_params) as db:
        db.execute(query)
        data = db.fetchall()

    return data

@mcp.tool(name="show_candles",description="This tool provide candlesticks")
def show_candlesticks(query:str):
    """
    This tool is called when user asks for recommendations on any stock.

    if user asks what is view on this stock or can I buy this stock or what is the view on this stock.

    Args : query

    Return : image
    """

@mcp.tool(name="read_pdfs", description="This tool helps to read pdf and return pdf data")
def read_pdfs(file_path):
    loader = PyMuPDFLoader(file_path)
    pages = [doc for doc in loader.lazy_load()]
    return pages

# @mcp.tool(description="This tool helps to industry related stocks")
# async def fetch_industrial_stocks():
#     """

#     This tool use when user query data related to industry or sector

#     Return : returns string

#     """
#     loader = WebBaseLoader("https://fyers.in/stock/")
#     docs = []
#     async for doc in loader.alazy_load():
#         docs.append(doc)
#     print(docs[0].page_content[:100])
#     print(docs[0].metadata)



if __name__ == "__main__":
    mcp.run(transport="stdio")

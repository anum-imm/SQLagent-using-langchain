
from langchain_core.tools import Tool
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate


def list_tables_tool(db: SQLDatabase):
    """
    Tool that lists all tables in the database.
    """
    return Tool(
        name="sql_db_list_tables",
        description="List all tables in the SQL database. Input can be any string.",
        func=lambda _: f"Tables: {', '.join(db.get_usable_table_names())}"
    )


def get_schema_tool(db: SQLDatabase):
    """
    Tool that fetches schema (CREATE TABLE statements) for given tables.
    """
    return Tool(
        name="sql_db_schema",
        description="Get SQL schema (CREATE TABLE statements) for tables. Input should be a comma-separated list of table names.",
        func=lambda table_names_str: (
            "No table names provided."
            if not any(name.strip() for name in table_names_str.split(","))
            else db.get_table_info(
                [name.strip() for name in table_names_str.split(",") if name.strip()]
            )
        )
    )


def query_tool(db: SQLDatabase):
    """
    Tool that executes a SQL query on the database.
    """
    return Tool(
        name="sql_db_query",
        description="Run a SQL query on the database. Input should be a SQL string.",
        func=lambda query: (
            "No SQL query provided."
            
        )
    )


def query_checker_tool(llm):
    """
    Tool that checks/improves a SQL query using an LLM.
    """
    return Tool(
        name="sql_db_query_checker",
        description=(
            "Check and fix a SQL query using an LLM. If it is not related to SQL, "
            "politely ask the user to provide a valid SQL query."
        ),
        func=lambda query: (
            "No SQL query provided."
            if not query else check_query_with_llm(llm, query)
        )
    )


def check_query_with_llm(llm, query: str):
    """
    Use LLM to validate and improve a SQL query, or reject if irrelevant.
    """
    prompt_text = (
        "You are an expert SQL assistant. "
        "Your only task is to check the following SQL query for correctness and best practices. "
        "If it is correct, just return it as-is. "
        "If it is incorrect or suboptimal, rewrite it correctly and explain briefly what was wrong. "
        "If the input is NOT a valid SQL query at all, "
        "politely reply: 'I can only help with SQL queries. Please provide a SQL statement.'\n\n"
        f"Query:\n{query}"
    )

    response = llm.invoke(prompt_text)
    return response.content


def get_custom_sql_tools(db: SQLDatabase, llm):
    """
    Return all custom SQL tools as a list.
    """
    tools = [
        list_tables_tool(db),
        get_schema_tool(db),
        query_tool(db),
        query_checker_tool(llm),
    ]

    print("✅ Custom SQL Tools available:")
    for t in tools:
        print(f"- {t.name}: {t.description}")

    return tools

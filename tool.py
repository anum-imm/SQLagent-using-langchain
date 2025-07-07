from langchain_community.utilities import SQLDatabase
from langchain_community.tools import (
    QuerySQLDatabaseTool,
    InfoSQLDatabaseTool,
    QuerySQLCheckerTool,
)
from langchain_core.tools import Tool

def get_sql_tools(db: SQLDatabase, llm):
    """
    Returns tools with names that match the agent prompt:
    """
    raw_tools = {
        "sql_db_list_tables": InfoSQLDatabaseTool(db=db),
        "sql_db_schema": InfoSQLDatabaseTool(db=db),
        "sql_db_query": QuerySQLDatabaseTool(db=db),
        "sql_db_query_checker": QuerySQLCheckerTool(db=db, llm=llm),
    }

    tools = [
        Tool(
            name=name,
            description=raw.description,
            func=raw.run
        )
        for name, raw in raw_tools.items()
    ]

    print("SQL Tools available:")
    for t in tools:
        print(f"- {t.name}: {t.description}")

    return tools




def fetch_table_schema(db, table_name: str) -> str:
    rows = db.run(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
        """,
        (table_name,),
    )
    if not rows:
        return f"No such table: {table_name}"
    lines = ["column_name | data_type       | nullable | default", "-"*50]
    for name, typ, nullable, default in rows:
        lines.append(f"{name:<12} | {typ:<14} | {nullable:<8} | {default or ''}")
    return "\n".join(lines)
 
def schema_tool_func(table_name: str) -> str:
    return fetch_table_schema(schema_tool_func.db, table_name)

# # from langchain_community.utilities import SQLDatabase
# # from langchain_community.tools import (
# #     QuerySQLDatabaseTool,
# #     InfoSQLDatabaseTool,
# #     QuerySQLCheckerTool,
# # )
# # from langchain_core.tools import Tool

# # def get_sql_tools(db: SQLDatabase, llm):
# #     """
# #     Returns tools with names that match the agent prompt:
# #     """
# #     raw_tools = {
        
# #         "sql_db_schema": InfoSQLDatabaseTool(db=db),
# #         "sql_db_list_tables": InfoSQLDatabaseTool(db=db),
# #         "sql_db_query_checker": QuerySQLCheckerTool(db=db, llm=llm),
# #         "sql_db_query": QuerySQLDatabaseTool(db=db),
# #     }

# #     tools = [
# #         Tool(
# #             name=name,
# #             description=raw.description,
# #             func=raw.run
# #         )
# #         for name, raw in raw_tools.items()
# #     ]

# #     print("SQL Tools available:")
# #     for t in tools:
# #         print(f"- {t.name}: {t.description}")

# #     return tools


# from typing import Optional, List 
# from langchain_community.utilities import SQLDatabase
# from langchain_core.tools import Tool

# def get_schema_tool(db: SQLDatabase) :
#     """
#     Tool: Get schema for specified tables.
#     If found → show schema.
#     If not found → 'Table not found: …'
#     """

#     return Tool(
#         name="sql_db_schema",
#         description="Get schema for specified tables. Input: comma-separated table names.",
#         func=lambda table_names: (
#             "No tables specified."
#             if not table_names.strip()
#             else "\n\n".join([
#                 db.get_table_info(name.strip())
#                 if db.get_table_info(name.strip())
#                 else f"Table not found: {name.strip()}"
#                 for name in table_names.split(",") if name.strip()
#             ])
#         )
#     )

# def list_tables_tool(db: SQLDatabase):
#     """
#     Tool that lists all tables in the database.
#     """
#     return Tool(
#         name="sql_db_list_tables",
#         description="List all tables in the SQL database. Input can be any string.",
#         func=lambda _: f"Tables: {', '.join(db.get_usable_table_names())}"
#     )

# def query_checker_tool(db: SQLDatabase, llm, query: str, verbose: bool = False) -> str:
#     """
#     Validates a SQL query through dry-run and LLM check.
#     Returns "VALID" or error message.
    
#     Args:
#         db: SQLDatabase connection
#         llm: Language model for logical validation
#         query: SQL query to validate
#         verbose: Whether to print validation steps
    
#     Returns:
#         Validation result ("VALID" or error message)
#     """
#     if verbose:
#         print(f"🔎 Validating query: {query[:100]}...")  # Print first 100 chars
    
#     # Dry-run syntax check
#     try:
#         if verbose:
#             print("  🛠️ Performing dry-run syntax check...")
#         db.run(query, dry_run=True)
#     except Exception as e:
#         if verbose:
#             print(f"  ❌ Syntax check failed: {str(e)}")
#         return f"Syntax Error: {str(e)}"
    
#     # LLM logical validation
#     if verbose:
#         print("  🤖 Performing LLM logical validation...")
    
#     prompt = f"""Check this SQL query for logical errors:
#     {query}
    
#     Respond ONLY with "VALID" if correct or specific error if invalid."""
    
#     try:
#         response = llm.invoke(prompt)
#         if "VALID" in response.upper():
#             if verbose:
#                 print("  ✅ Query is valid")
#             return "VALID"
#         else:
#             if verbose:
#                 print(f"  ⚠️ Logical issues found: {response}")
#             return f"Validation Error: {response}"
#     except Exception as e:
#         if verbose:
#             print(f"  ❗ LLM validation failed: {str(e)}")
#         return f"LLM Error: {str(e)}"

# def query_tool(db: SQLDatabase):
#     """
#     Tool that executes a SQL query on the database.
#     """
#     return Tool(
#         name="sql_db_query",
#         description="Run a SQL query on the database. Input should be a SQL string.",
#         func=lambda query: (
#             "No SQL query provided."
            
#         )
#     )


# def get_sql_tools(db: SQLDatabase, llm):
#     """
#     Return all custom SQL tools as a list.
#     """
#     tools = [
#         list_tables_tool(db),
#         get_schema_tool(db),
#         query_tool(db),
#         query_checker_tool(llm),
#     ]

#     print("✅ Custom SQL Tools available:")
#     for t in tools:
#         print(f"- {t.name}: {t.description}")

#     return tools



# 💼 MCP Financial Agent

An intelligent financial query agent powered by [LangGraph](https://www.langchain.com/langgraph), [Gemini LLM].  
This agent converts natural language queries into SQL, verifies stock symbols, fetches financial insights from a PostgreSQL database, and can parse business PDFs such as DRHPs for investment signals.

---

## 🚀 Features

- ✅ **Natural Language to SQL**: Converts finance-related queries into valid SQL using Gemini LLM.
- ✅ **Symbol Verification Tool**: Parses symbol-to-stock mappings from JSON for accurate results.
- ✅ **Schema Introspection**: Dynamically understands table structure before generating queries.
- ✅ **PDF Analysis**: Reads and interprets quarterly results and financial metrics from PDF files (e.g., DRHP).
- ✅ **Real-time Reasoning**: Built using `LangGraph` and `FastMCP` with agent memory.
- ✅ **Secure Query Execution**: Enforces read-only access, SQL safety, and query constraints.
- ✅ **Tool Orchestration**: Powered by `create_react_agent()` with multi-tool workflow.

---

## 🧠 Tech Stack

| Component        | Details |
|------------------|---------|
| LLM              | Google Gemini 2.5 (via LangChain) |
| Agent Framework  | LangGraph + LangChain |
| Protocol         | Model Context Protocol (MCP) |
| Backend Tools    | FastMCP, PostgreSQL, JSON, PyMuPDF |
| Data Layer       | Local PostgreSQL (financial schema) |
| PDF Parser       | `PyMuPDFLoader` from LangChain |
| Query Transport  | `stdio` client-server interaction |

---


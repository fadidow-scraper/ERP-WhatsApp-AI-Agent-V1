# ERP WhatsApp AI Agent (V1)

An intelligent automation agent that bridges corporate ERP backend data with WhatsApp to deliver autonomous customer support and real-time business insights.

## Features
- Asynchronous Communication: Built handling real-time unstructured user queries via WhatsApp.
- LLM Integration and Tool-Chaining: Leverages Gemini and OpenRouter APIs paired with structured prompt engineering to act as an autonomous support assistant.
- Live Database Lookups: Parses user intents to execute secure, real-time SQL queries on the ERP database to fetch invoice data, order tracking, and inventory status.
- Robust Error Handling: Implements retry logic and fallbacks for failed API requests or ambiguous user intents.

## Tech Stack
- Language: Python 3.x
- APIs: OpenAI/Gemini, OpenRouter API, Twilio API (WhatsApp Gateway)
- Database: SQLite / PostgreSQL (SQLAlchemy ORM)
- Asynchronous Tools: Asyncio

## Project Structure
- main.py: Application entry point and server setup.
- ai_logic.py: Core AI logic, prompt structures, and LLM orchestration.
- database.py: SQL database configurations and queries.
- config.py: Environment variables and API key configurations.

## Security Notice
All API keys and database credentials are managed strictly via environment variables (.env). No sensitive keys are hardcoded.

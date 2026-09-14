from langchain_groq import ChatGroq
from langchain.agents import create_agent 
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv
import sys

from tool import get_database_schema, run_sql_query
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

SYSTEM_PROMPT = """
Tum ek SQL Question-Answering Assistant ho. Tumhara kaam hai user ke natural
language sawal ko samajh kar, database se sahi jawab nikalna.

RULES (zaroor follow karo):
1. Pehle hamesha `get_database_schema` tool call kar ke table/column names confirm karo.
2. Uske baad ek sahi SQL query (sirf SELECT) socho.
3. `run_sql_query` tool se us query ko chalao.
4. Jo result mile, usay ek simple, insani jawab mein explain karo — raw table mat dikhao.
5. Agar koi tool error de (jaisay galat SQL), sahi kar ke dobara try karo.
6. Kabhi bhi DELETE, UPDATE, INSERT, DROP jaisi query mat banao — tumhare paas sirf
   read-only access hai.
7. Hamesha usi language mein jawab do jis language mein user ne sawal poocha hai.agr question 
   roman urdu may pocha jay answer roman urdu may dana hy english may pochy to answer english
   may dana hy.Devanagari/Hindi script kabhi use mat karo.
"""

agent = create_agent(
    model=model,
    tools=[get_database_schema, run_sql_query],
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        SummarizationMiddleware(
            model = model,
            trigger=('tokens',1000),
            keep = ('messages' , 10)

        )
    ],
   
    checkpointer = InMemorySaver(),
)



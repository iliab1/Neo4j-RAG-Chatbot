from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField, RunnableParallel
from langchain_openai import ChatOpenAI

from neo4j_advanced_rag.retrievers import (
    hypothetic_question_vectorstore,
    parent_vectorstore,
    summary_vectorstore,
    typical_rag,
)
# For message history
from pydantic import BaseModel
from typing import List, Union
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


template = """Answer the question based only on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

retriever = typical_rag.as_retriever().configurable_alternatives(
    ConfigurableField(id="strategy"),
    default_key="typical_rag",
    parent_strategy=parent_vectorstore.as_retriever(),
    hypothetical_questions=hypothetic_question_vectorstore.as_retriever(),
    summary_strategy=summary_vectorstore.as_retriever(),
)

# Handle the contextualization of the question
# Used https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/ as a reference
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

# Define the prompt template
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),  # "chat_history": itemgetter("chat_history")
        ("human", "{question}"),  # "question": itemgetter("question")
    ]
)

# Contextualize chain
contextualize_runnable = (
    contextualize_q_prompt
    | model
    | StrOutputParser()
)

# Pass contextualize_chain output as variable called contextual_question
# Used https://www.reddit.com/r/LangChain/comments/1axhxg5/langchain_runnableparallel/ as a reference
contextualize_chain = RunnablePassthrough.assign(contextual_question=contextualize_runnable)

# Combine the chains
memory_chain = (
    contextualize_chain
    | RunnableParallel(
        {
            "context": itemgetter("contextual_question") | retriever | format_docs,
            "question": itemgetter("contextual_question"),
        }
    )
    | prompt
    | model
    | StrOutputParser()
)


# Add typing for input
class Question(BaseModel):
    question: str
    chat_history: List[Union[AIMessage, HumanMessage]]


chain_with_memory = memory_chain.with_types(input_type=Question)

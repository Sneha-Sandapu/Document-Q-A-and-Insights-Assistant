from langchain.prompts import ChatPromptTemplate, PromptTemplate

qa_system_prompt = """You are an intelligent document assistant designed to extract information and provide insights based on the provided document context.
Use the following pieces of retrieved context to answer the question.
If the information is not in the context, just say that you don't know based on the document. Do not guess.
Provide a clear, detailed, and context-aware answer.

Context: {context}
"""

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    ("human", "{input}"),
])

summary_prompt = """You are an expert summarizer. Write a comprehensive summary of the following document content.
Highlight the key points, main arguments, and any important insights.

Document Content:
"""
"{text}"""
"""
CONCISE SUMMARY:
"""

SUMMARY_PROMPT = PromptTemplate.from_template(summary_prompt)

ROUTING_PROMPT = """You are a routing agent. Your job is to decide whether the user's query is asking for a general 'SUMMARY' of the document, or a 'QA' (specific question) about the document's contents.
Respond with EXACTLY ONE WORD: either 'SUMMARY' or 'QA'. Do not include any punctuation or extra words.

User Query: {query}
ROUTE:"""

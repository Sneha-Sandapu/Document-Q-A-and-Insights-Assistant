import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from prompts import QA_PROMPT, ROUTING_PROMPT
from langchain.prompts import PromptTemplate

def get_vector_store(text_chunks):
    """Create and return a FAISS vector store from text chunks."""
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_llm():
    """Return the LLM instance to use across chains."""
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

def route_query(query: str):
    """Determine if the query is asking for a general SUMMARY or specific QA."""
    llm = get_llm()
    prompt = PromptTemplate.from_template(ROUTING_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"query": query})
    return result.content.strip().upper()

def get_summary(text_chunks):
    """Generate a map-reduce summary of the entire document."""
    llm = get_llm()
    docs = [Document(page_content=t) for t in text_chunks]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.invoke({"input_documents": docs})
    return summary["output_text"]

def answer_query(query, vector_store):
    """Answer a specific question based on vector store context using Retrieval."""
    llm = get_llm()
    document_chain = create_stuff_documents_chain(llm, QA_PROMPT)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    response = retrieval_chain.invoke({"input": query})
    return response["answer"]

def process_user_input(query, vector_store, text_chunks):
    """Multi-step agentic workflow to route and process user input."""
    route = route_query(query)
    
    if "SUMMARY" in route:
        return get_summary(text_chunks), "Summary"
    else:
        return answer_query(query, vector_store), "QA"

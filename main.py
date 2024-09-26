from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import CharacterTextSplitter

model_local = ChatOllama(model="llama3.2")

# 1. Split data into chunks
text_data = """
Security Report for Project: 'XYZ Web Application'

Date: September 26, 2024
Report Prepared by: John Doe
1. Executive Summary

This report outlines the results of the security assessment performed on the XYZ Web Application. The assessment identified several critical, high, medium, and low-risk vulnerabilities. Immediate action is required to mitigate critical and high-risk vulnerabilities to safeguard sensitive information and ensure regulatory compliance.
2. Scope of the Assessment

    System Evaluated: XYZ Web Application (Version 1.2.0)
    Components Included:
        Web Application Frontend
        API Services
        Database Server
    Test Type: Manual and Automated Penetration Testing
    Testing Period: September 10–September 24, 2024

3. Findings Summary
Risk Level	Number of Issues
Critical	2
High	4
Medium	6
Low	8
Informational	3
4. Critical Vulnerabilities
4.1. SQL Injection in Login Functionality

    Vulnerability ID: XYZ-2024-001
    Description: An attacker can perform SQL injection through the login form, potentially allowing unauthorized access to the database.
    Affected Components: User Login API
    Risk Level: Critical
    Recommendation: Sanitize and parameterize SQL queries to prevent injection.

4.2. Remote Code Execution via File Upload

    Vulnerability ID: XYZ-2024-002
    Description: The file upload feature allows arbitrary file types, enabling attackers to upload malicious scripts that could lead to remote code execution.
    Affected Components: File Upload Service
    Risk Level: Critical
    Recommendation: Implement strict file type validation and execute uploaded files in a sandboxed environment.

5. High-Risk Vulnerabilities
5.1. Cross-Site Scripting (XSS)

    Vulnerability ID: XYZ-2024-003
    Description: The application is vulnerable to XSS attacks, where attackers can inject malicious scripts into user inputs.
    Affected Components: Search Functionality
    Risk Level: High
    Recommendation: Sanitize all user inputs and apply Content Security Policy (CSP) headers.

5.2. Weak Encryption for Sensitive Data

    Vulnerability ID: XYZ-2024-004
    Description: Sensitive user information is encrypted using weak algorithms that are susceptible to modern attacks.
    Affected Components: User Authentication Service
    Risk Level: High
    Recommendation: Upgrade to stronger encryption algorithms such as AES-256.

6. Remediation Plan
Vulnerability ID	Priority	Assigned To	Estimated Fix Date
XYZ-2024-001	Critical	Dev Team A	October 1, 2024
XYZ-2024-002	Critical	Dev Team B	October 3, 2024
XYZ-2024-003	High	Dev Team C	October 7, 2024
XYZ-2024-004	High	Dev Team D	October 5, 2024
7. Conclusion

The XYZ Web Application contains critical vulnerabilities that could lead to severe data breaches and system compromise. Immediate remediation is recommended for all critical and high-risk vulnerabilities. A follow-up review will be scheduled for November 2024 to reassess the effectiveness of the implemented fixes.
"""
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=7500, chunk_overlap=100)
doc_splits = text_splitter.split_text(text_data)

# 2. Convert documents to Embeddings and store them
vectorstore = Chroma.from_texts(
    texts=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings.OllamaEmbeddings(model='nomic-embed-text'),
)
retriever = vectorstore.as_retriever()

# 3. Prompt the model and output the result
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)
result = after_rag_chain.invoke("Write a one paragraph summary of the context") 
print()
print(result)

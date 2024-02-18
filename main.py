from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA

pdfs = "./pdfs/"
output = "vectorstore/db_faiss"

def create_vector_db():
    loader = DirectoryLoader(pdfs,glob="*.pdf",loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    
    db = FAISS.from_documents(texts,embeddings)
    db.save_local(output)


def create_prompt():
    custom_prompt_template = """Use the following pieces of information to answer the user's question regarding malware analysis.
If the question is not realted to malware analysis, or you don't know the answer, or if you can not find the relevant info in the source document 'pdfs/Malware Analysis Steps & Examples - CrowdStrike.pdf',
 just say that you don't know, don't try to make up an answer.

context: {context}
Question: {question}
Only return the helpful answer and nothing else.
Helpful answer:
"""
    prompt=PromptTemplate(template=custom_prompt_template,
                          input_variables=['context','question'])
    return prompt

def create_qa_chain(llm,prompt,db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain

def load_module():

    # loading the metas llama LLM
    print("Loading LLM")
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_token=512,
        temperature=0.5,
        #config={"gpu_layers":3}, # for some reason GPU does not work for me
    )
    print("LLM Loaded")
    print("Loading embeddings")
    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device':'cpu'}
    )
    db = FAISS.load_local(output,embeddings)
    print("embeddings DB loaded")

    qa=create_qa_chain(llm,create_prompt(),db)
    print("custom chain created")
    return qa

def main():
    llm = load_module()
    print(llm({'query':"what is malware analysis?"}))
    print(llm({'query':"How to treat tounge infection disease?"}))
    #print(llm({'query':"Why are stars so bright?"}))
   #create_vector_db()

main()
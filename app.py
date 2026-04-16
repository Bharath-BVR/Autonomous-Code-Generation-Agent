import streamlit as st  
# streamlit library used to create web interface for AI agent

import sys  
# provides access to system-specific parameters and functions

import os  
# used for file and directory operations


#sys.path.append(os.path.dirname(os.path.abspath(__file__)))  
# adds current project directory to system path
# allows python to import local modules correctly


from agent.github_retriever import search_github  
# imports function to retrieve repositories from GitHub

from vector_store.faiss_store import VectorStore  
# imports vector database class used for semantic search

from agent.code_generator import generate_code  
# imports function that generates code using LLM

from agent.code_executor import execute_code  
# imports function that executes generated code using online compiler API

from agent.error_corrector import fix_code  
# imports function that fixes code errors using LLM

from agent.evaluator import evaluate_code  
# imports function that evaluates model performance

from config import MAX_FIX_ATTEMPTS  
# imports maximum number of retries allowed for fixing code errors


st.title("Autonomous Code Generation Agent")  
# displays title in Streamlit web UI


@st.cache_resource
def load_vector_db():
    # caches vector database so it does not reload repeatedly

    return VectorStore()
    # returns VectorStore object for semantic search


query = st.text_input("Enter coding problem")  
# creates text input box for user query


if st.button("Generate"):
    # runs when user clicks Generate button

    if query.strip() == "":
        # checks if input is empty

        st.warning("Enter a query")
        # shows warning message in UI

        st.stop()
        # stops execution if query is empty


    with st.spinner("Generating code..."):
        # shows loading spinner while processing

        # GitHub search
        repos = search_github(query)
        # retrieves GitHub repositories related to query


        # prepare context
        docs = [
            # prepares text documents for embedding

            f"{repo['name']} {repo['description']} {repo['url']}"
            # combines repo name, description and url into single text

            for repo in repos
            # iterates through retrieved repositories
        ]


        if len(docs) == 0:
            # if no repositories retrieved

            docs = [query]
            # fallback: use user query as context


        vector_db = load_vector_db()
        # loads cached vector database


        vector_db.index.reset()
        # clears existing embeddings index


        vector_db.texts = []
        # clears stored text documents


        vector_db.add_documents(docs)
        # converts documents into embeddings and stores them in FAISS index


        context = vector_db.search(query)
        # retrieves most relevant context using similarity search


        # generate code
        language, code = generate_code(query, context)
        # calls LLM to generate programming language and code


        # execute python code only
        output, error = execute_code(language, code)
        # executes generated code using online compiler API


        # fixed correction loop errors
        #if error:
            #for _ in range(MAX_FIX_ATTEMPTS):
                #code = fix_code(code, error)
                #output, error = execute_code(code)
                #if error == "":
                   # break


        ##########################################
        ### CHANGED: dynamic correction loop ###
        ##########################################

        attempt = 0
        # initialize counter for correction attempts


        while error != "" and attempt < MAX_FIX_ATTEMPTS:
            # loop continues until no error or max attempts reached

            code = fix_code(code, error)
            # sends code and error to LLM for correction

            output, error = execute_code(language, code)
            # executes corrected code again

            attempt += 1
            # increases attempt counter


        metrics = evaluate_code(query, code, error, context)
        # evaluates model performance using defined metrics


    st.subheader("Generated Code")
    # displays subtitle in UI

    st.code(code)
    # shows generated code in formatted code block


    #st.subheader("Error")
    # commented out section for displaying error message


    #st.write(error if error else "No error")
    # displays error output (currently disabled)


    #st.subheader("Evaluation Metrics")
    # commented out section for displaying evaluation scores


    #st.json(metrics)
    # displays evaluation metrics in JSON format (currently disabled)


    #st.subheader("GitHub References")
    # commented out section for displaying GitHub repository links


    #if len(repos) == 0:
    # checks if no GitHub repositories found


        #st.write("No repositories found")
        # displays message if no repositories available


    #else:
    # executes when repositories exist


        #for repo in repos:
        # iterates through repositories


           # st.write(repo["url"])
           # displays GitHub repository links
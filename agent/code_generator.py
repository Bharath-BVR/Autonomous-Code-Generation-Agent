import ollama  
# library used to interact with local LLM models running via Ollama

from config import LLM_MODEL  
# imports model name (for example phi3, tinyllama) from config file


def generate_code(query, context):
    # function that generates code using LLM
    # query → user request (example: "write python code for fibonacci")
    # context → retrieved GitHub knowledge used for RAG


    context_text = "\n".join(context) if context else ""
    # converts list of context documents into single string
    # joins each context item with newline
    # if no context available, use empty string


    prompt = f"""
Generate the code for the request below using GitHub knowledge if relevant.

Output format:
<language>
<code>

GitHub context:
{context_text}

Request:
{query}
"""

    response = ollama.chat(
        # calls Ollama API to interact with LLM

        model=LLM_MODEL,
        # specifies which LLM to use (phi3, tinyllama, deepseek-coder, etc.)

        messages=[
            {
                "role": "user",
                "content": prompt
                # sends prompt as user message to LLM
            }
        ]
    )


    text = response["message"]["content"].strip()
    # extracts generated response text from LLM output
    # .strip() removes extra spaces or newline characters


    lines = text.split("\n")
    # splits LLM output into multiple lines


    language = lines[0].strip().lower()
    # first line contains programming language name
    # example: python, java, c
    # strip removes spaces
    # lower converts to lowercase for consistency


    code = "\n".join(lines[1:])
    # remaining lines contain generated code
    # joins them back into single code block


    return language, code
    # returns detected programming language and generated code
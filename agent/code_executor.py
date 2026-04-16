import requests   # library used to send HTTP requests to external APIs


def execute_code(language, code):
    # function that sends code to an online compiler API
    # language → programming language (python, java, c, etc.)
    # code → generated code from LLM

    url = "https://emkc.org/api/v2/piston/execute"
    # API endpoint for Piston online compiler which supports multiple languages

    payload = {
        # request body sent to API

        "language": language,
        # specifies which programming language to execute

        "version": "*",
        # tells API to use default/latest version of the language

        "files": [
            # API expects code in file format

            {
                "content": code
                # actual generated code content sent for execution
            }

        ]
    }

    try:
        # try block used to handle API errors safely

        response = requests.post(url, json=payload, timeout=20)
        # send POST request to API
        # json=payload → sends code data
        # timeout=20 → wait maximum 20 seconds for response

        result = response.json()
        # convert API response into python dictionary format

        output = result.get("run", {}).get("stdout", "")
        # extract standard output produced by executed code
        # example: print() results
        # .get() avoids error if key is missing

        error = result.get("run", {}).get("stderr", "")
        # extract error message if execution fails
        # example: syntax error, runtime error

        return output, error
        # return execution result and error message


    except Exception as e:
        # catches network issues, API errors, timeout errors

        return "", str(e)
        # return empty output and error description
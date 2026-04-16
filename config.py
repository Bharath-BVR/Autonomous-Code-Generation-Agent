# GitHub API endpoint
# chosen because GitHub provides real code knowledge base
GITHUB_API = "https://api.github.com/search/repositories"

# model name from ollama
# deepseek-coder selected because it performs very well in code tasks compared to other free models
#LLM_MODEL = "deepseek-coder:1.3b"
LLM_MODEL = "phi3"

# number of repositories retrieved
TOP_K = 3

# number of correction attempts
MAX_FIX_ATTEMPTS = 10
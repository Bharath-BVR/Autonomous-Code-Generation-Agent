# Autonomous Code Generation Agent using GitHub Knowledge Base

## Overview

This project builds an AI agent system capable of generating executable code using GitHub as a knowledge base.

The system follows a Retrieval-Augmented Generation (RAG) architecture where:

1. Relevant repositories are retrieved from GitHub
2. Repository text is converted into embeddings
3. Semantic search retrieves the most relevant context
4. LLM generates code using the retrieved GitHub knowledge
5. Generated code is executed using an online compiler API
6. If errors occur, the agent automatically corrects the code

This approach reduces hallucination and improves code quality by grounding responses in real GitHub knowledge.

---

## Key Features

- Uses GitHub as real-world coding knowledge base
- Supports multiple programming languages
- Retrieval-Augmented Generation (RAG)
- Semantic similarity search using embeddings
- Automatic error correction loop
- Online code execution via API
- GitHub response caching
- Persistent vector storage
- Model evaluation metrics
- Streamlit UI

---

## Architecture Diagram

```
+-------------------+
| User Query        |
+---------+---------+
          |
          v
+-------------------+
| GitHub Retriever  |
| (GitHub API)      |
+---------+---------+
          |
          v
+---------------------------+
| Embedding Model           |
| sentence-transformers     |
+---------+-----------------+
          |
          v
+---------------------------+
| Vector Store              |
| FAISS                     |
+---------+-----------------+
          |
          v
+---------------------------+
| Context Retrieval         |
| Semantic Similarity       |
+---------+-----------------+
          |
          v
+---------------------------+
| LLM (Ollama)              |
| Code Generation           |
+---------+-----------------+
          |
          v
+---------------------------+
| Online Compiler API       |
| Piston API                |
+---------+-----------------+
          |
          v
+---------------------------+
| Error Correction Loop     |
| LLM fixes code            |
+---------+-----------------+
          |
          v
+---------------------------+
| Evaluation Metrics        |
| Accuracy + Hallucination  |
+---------+-----------------+
          |
          v
+---------------------------+
| Streamlit UI              |
+---------------------------+
```

---

## Project Structure

```
autonomous-code-agent/
│
├── agent/
│   ├── code_generator.py
│   ├── code_executor.py
│   ├── error_corrector.py
│   ├── evaluator.py
│   ├── github_retriever.py
│
├── vector_store/
│   ├── faiss_store.py
│
├── config.py
├── app.py
├── requirements.txt
├── github_cache.pkl
├── faiss_index.bin
├── faiss_texts.pkl
└── README.md
```

---

## Technologies Used

| Component | Technology |
|----------|------------|
| LLM -> Ollama |
| Embeddings -> sentence-transformers |
| Vector Database -> FAISS |
| Knowledge Source -> GitHub API |
| Code Execution -> Piston API |
| UI -> Streamlit |
| Language -> Python |

---

## Installation

### Step 1: Clone repository

```
git clone <repository_url>
cd autonomous-code-agent
```

---

### Step 2: Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### Step 3: Install dependencies

```
pip install -r requirements.txt
```

---

### Step 4: Install LLM model

```
ollama pull phi3
```

or faster model:

```
ollama pull phi3
```

---

## Run Application

```
streamlit run app.py
```

Open browser:

```
http://localhost:8501
```

---

## Example Queries

```
write python code for fibonacci

write java program for binary search

create c program to add two numbers

write javascript function for factorial

write sql query to find duplicates
```

---

## How it Works

Step 1: GitHub Retrieval  
Relevant repositories are fetched using GitHub API.

Step 2: Embedding Generation  
Repository descriptions are converted into embeddings using sentence-transformers.

Step 3: Vector Similarity Search  
FAISS finds the most relevant GitHub knowledge.

Step 4: Code Generation  
LLM generates code using retrieved context.

Step 5: Code Execution  
Generated code is executed using Piston API.

Step 6: Self Correction  
If error occurs, LLM fixes the code automatically.

Step 7: Evaluation  
Model performance is evaluated using defined metrics.

---

## Evaluation Metrics

| Metric | Description |
|-------|-------------|
| compilation_success -> code executes without error |
| code_generated -> model produces valid code |
| relevance_score -> generated code matches query |
| hallucination_score -> detects unrelated content |
| github_grounding ->| verifies GitHub knowledge usage |
| final_score -> overall accuracy |

Final score formula:

```
final_score =
(
 compilation_success
 + code_generated
 + relevance_score
 + hallucination_score
 + github_grounding
) / 5
```

---

## Latency Optimization

Latency is reduced using:

- GitHub response caching
- persistent FAISS vector store
- lightweight embedding model
- optimized prompt size
- limited retry attempts

Cached files:

```
github_cache.pkl
faiss_index.bin
faiss_texts.pkl
```

---

## Why RAG (Retrieval-Augmented Generation)

LLMs may hallucinate incorrect code.

Using GitHub as knowledge base:

- improves reliability
- reduces hallucination
- provides real-world coding patterns
- improves accuracy

---
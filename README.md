# Portfolio Analysis with RAG

## Overview

This project provides a system for analyzing mutual fund portfolio data using a Retrieval Augmented Generation (RAG) approach. Users can ask questions in natural language about the fund data, and the system will retrieve relevant information and generate a comprehensive answer.

The primary goal is to make mutual fund data more accessible and easier to interrogate by leveraging local Large Language Models (LLMs) for understanding queries and generating human-like responses based on the provided data. It utilizes Ollama for running LLMs locally and FAISS for creating an efficient searchable vector store of the fund data.

## Core Functionality

The system operates in two main stages:

1.  **Data Ingestion and Vector Store Creation**:
    *   Mutual fund portfolio data, available in CSV format, is loaded and processed.
    *   The data is split into manageable chunks.
    *   Embeddings are generated for each chunk using an Ollama embedding model (`nomic-embed-text`).
    *   These embeddings are stored in a FAISS vector store, allowing for efficient similarity searches. This process is handled by `add_data_tovector_db_csv.py`.

2.  **Question Answering via RAG**:
    *   The user inputs a question about the mutual funds.
    *   The system retrieves the most relevant data chunks from the FAISS vector store based on the semantic similarity of the question.
    *   The retrieved chunks (context) and the original question are then fed to an Ollama language model (`llama3.2:3b`).
    *   The LLM generates a comprehensive answer based on the provided context and question. This interactive Q&A is handled by `MFAnalyser.py`.

## Key Scripts

### `add_data_tovector_db_csv.py`

*   **Purpose**: This script is responsible for processing input CSV files containing mutual fund data, generating embeddings, and building a FAISS vector store.
*   **Key Libraries**: `pandas`, `python-dotenv`, `langchain_ollama` (for `OllamaEmbeddings`), `langchain_community` (for `CSVLoader`, `FAISS`, `InMemoryDocstore`), `langchain_text_splitters`, `faiss-cpu`.
*   **Input**:
    *   CSV files (e.g., `Funds_Sept_2024.csv`, `Funds_Nov_2024.csv`).
    *   Currently, file paths are hardcoded. It's recommended to modify the script to use environment variables or command-line arguments for file paths.
*   **Process**:
    1.  Loads data from specified CSV files.
    2.  Splits the documents into smaller chunks for effective embedding and retrieval.
    3.  Uses the `nomic-embed-text` Ollama model to generate embeddings for each chunk.
    4.  Creates a FAISS index and stores the chunks and their embeddings.
*   **Output**: Saves the FAISS vector store to the `ZerodhaMidCapFunds/` directory (containing `index.faiss` and `index.pkl`).

### `MFAnalyser.py`

*   **Purpose**: This script provides an interactive command-line interface for users to ask questions about the mutual fund data.
*   **Key Libraries**: `faiss-cpu`, `langchain_ollama` (for `OllamaEmbeddings`, `ChatOllama`), `langchain_community` (for `FAISS`), `langchain_core`.
*   **Input**: User questions entered via the command line.
*   **Process**:
    1.  Loads the pre-built FAISS vector store from the `ZerodhaMidCapFunds/` directory.
    2.  Initializes an Ollama embedding model (`nomic-embed-text`) and a chat model (`llama3.2:3b`).
    3.  For each user question:
        *   Retrieves relevant document chunks from the vector store (k=3, meaning top 3 most similar chunks).
        *   Formats these chunks as context.
        *   Uses a predefined prompt template to combine the context and the user's question.
        *   Sends the combined prompt to the Ollama chat model to generate an answer.
    4.  Prints the generated answer to the console.
*   **Output**: Answers to user questions, printed to the console.

### `prompts.py`

*   **Purpose**: This file contains example string prompts (`prompt_2`, `prompt3`).
*   **Details**: These prompts demonstrate different ways to interact with language models, such as requesting structured output (JSON) or maintaining a consistent conversational style. They are not directly used in the main RAG pipeline (`MFAnalyser.py` or `add_data_tovector_db_csv.py`) but can be useful for testing, experimentation, or extending the functionality.

## Data Files and Directories

*   **`ZN250 - Monthly Portfolio November 2024.xlsx`**
*   **`ZN250 - Monthly Portfolio September 2024.xlsx`**
    *   These Excel files appear to be the original source of the mutual fund portfolio data.
    *   The script `add_data_tovector_db_csv.py` currently expects data in CSV format (e.g., `Funds_Sept_2024.csv`, `Funds_Nov_2024.csv`). These CSVs are likely derived from these Excel files, though the conversion process is not included in this repository.

*   **`ZerodhaMidCapFunds/`**
    *   This directory stores the FAISS vector database.
    *   **`index.faiss`**: The actual FAISS index containing the vector embeddings.
    *   **`index.pkl`**: A pickle file storing associated document information (docstore) and mappings for the FAISS index.
    *   This directory is created by `add_data_tovector_db_csv.py` and read by `MFAnalyser.py`. You should not need to modify its contents manually.

## Setup and Usage

### Prerequisites

1.  **Python**: Ensure you have Python 3.8+ installed.
2.  **Ollama**:
    *   Install Ollama from [ollama.com](https://ollama.com/).
    *   Pull the required models:
        ```bash
        ollama pull nomic-embed-text:latest
        ollama pull llama3.2:3b 
        ```
    *   Ensure Ollama is running before executing the scripts.
3.  **Python Dependencies**: Install the necessary Python packages. It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    (Note: `requirements.txt` will be created as part of this process.)

### Configuration

1.  **Data Files**:
    *   The `add_data_tovector_db_csv.py` script currently hardcodes paths to input CSV files (e.g., `C:/Users/Atharva/Desktop/GitHubProjects/Funds_Sept_2024.csv`).
    *   **You will need to modify these paths** in `add_data_tovector_db_csv.py` to point to the location of your CSV data files.
    *   The CSV files should contain the mutual fund portfolio data. The structure is implicitly defined by how `CSVLoader` and the subsequent processing handle it.
2.  **(Optional) Environment Variables**:
    *   The script `add_data_tovector_db_csv.py` uses `load_dotenv()`. You can create a `.env` file in the root directory to manage any environment-specific configurations if needed (e.g., model names, alternative paths), though currently, it's not explicitly used for critical parameters like file paths.

### Running the System

1.  **Prepare Data & Build Vector Store**:
    *   Ensure your CSV data files are correctly referenced in `add_data_tovector_db_csv.py`.
    *   Run the script to process the data and create the FAISS vector store:
        ```bash
        python add_data_tovector_db_csv.py
        ```
        This will create the `ZerodhaMidCapFunds/` directory if it doesn't exist.

2.  **Analyze Data (Question Answering)**:
    *   Once the vector store is built, run the analyser script:
        ```bash
        python MFAnalyser.py
        ```
    *   The script will prompt you to "Enter your Question:". Type your question and press Enter.
    *   To exit the analyser, type "exit" and press Enter.

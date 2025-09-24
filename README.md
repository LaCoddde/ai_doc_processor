# AI Document Processor

## About The Project

This project is an intelligent document processing pipeline built locally to automatically extract key information from documents like certificates and IDs. The goal is to reduce manual data entry, improve accuracy, and learn key skills across the full product development lifecycle.

---

## Getting Started

### Prerequisites

* Python 3.8+
* An OpenAI API Key

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd ai_doc_processor
    ```

2.  **Create a virtual environment and install dependencies:**
    You can use the automated setup script:
    ```sh
    bash setup.sh
    ```
    Or run the commands manually:
    ```sh
    python3 -m venv ai_doc_venv
    source ai_doc_venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your API key:
    ```
    OPENAI_API_KEY='sk-...'
    ```

---

## Usage

To run the main analysis script:
```sh
python main.py
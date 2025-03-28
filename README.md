# Financial Reports Analysis Assistant

An AI-powered application that enables financial analysts to quickly extract relevant information from quarterly reports using natural language.

## Features

  - 📄 PDF Report Upload: Easily upload corporate quarterly reports
  - 🔍 Semantic Search: Find precise information without manually scanning hundreds of pages
  - 💬 Natural Language Queries: Ask questions like "What was the revenue this quarter?" or "How have margins evolved?"
  - 📊 Source Tracking: Always verify where information comes from with precise citations (page and document)
  - 🧠 Contextual Understanding: The system understands financial context and generates relevant answers

## Architecture

This project uses a RAG (Retrieval-Augmented Generation) architecture that combines semantic search and text generation:

  - Document Preprocessing: PDFs are converted to text and segmented into optimal chunks
  - Vectorization: Text is transformed into vector embeddings via OpenAI API
  - Vector Storage: Embeddings are stored in a Pinecone vector database
  - Semantic Queries: Questions are vectorized and compared to stored chunks
  - Augmented Generation: The LLM uses retrieved context to produce accurate answers

<img width="1118" alt="Screenshot 2025-03-28 at 12 12 44" src="https://github.com/user-attachments/assets/89abe91a-cda2-4471-834d-81cc5512ca69" />

## Installation
### Prerequisites

  - Python 3.10+
  - API keys for OpenAI and Pinecone

### Setup

 1- Clone the repository
```bash
git clone https://github.com/yourusername/fin-reports-assistant.git
cd fin-reports-assistant
```
 2- Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
 3- Install dependencies
```bash
pip install -r requirements.txt
```

 4- Create and configure your API keys
Create a .env file in the root directory with the following content:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

 5- Create a Pinecone index

  - Log in to your Pinecone account
  - Create a new index named finacial-reports (or update the INDEX_NAME in config.py)
  - Set the dimension to 1024 for OpenAI embeddings
  - Choose cosine as the metric


 6- Launch the application
 ```bash
streamlit run src/app.py
```

## Usage

  1- Upload Documents: Use the sidebar to upload one or more financial reports (PDF)
  2- Indexing: Click "Process Documents" to index the content
  3- Querying: Ask your question in the main text area or use the suggested questions
  4- Analyze Responses: Review the generated answer and check the sources for validation

Project Structure
```
fin-reports-assistant/
│
├── data/                         # Temporary storage for PDF reports
│
├── src/                          # Source code
│   ├── app.py                    # Streamlit interface
│   ├── config.py                 # Configuration and environment variables
│   ├── document_loader.py        # PDF loading and preprocessing
│   ├── qa_chain.py               # Question-answering pipeline
│   └── vectorstore.py            # Vector database management
│
├── .env                          # Environment variables (not versioned)
├── .gitignore                    # Files excluded from versioning
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
└── LICENCE.md                    # Licence file
```
## Technologies Used

  - LangChain: Orchestration of the RAG pipeline
  - OpenAI: API for embeddings and text generation
  - Pinecone: Vector database
  - Streamlit: Interactive user interface
  - PyPDF: Text extraction from PDFs

## Potential Applications and Future Improvements
This project serves as a foundation for a robust financial analysis assistant that can be significantly enhanced:
### Enterprise Integration

  - #### Self-hosted LLM deployment:
Replace OpenAI with open-source models like Llama, Mistral, or Falcon deployed on private infrastructure for enhanced data privacy and reduced operational costs
  - #### On-premise vector database:
Transition from Pinecone to a self-hosted vector database like Weaviate or Qdrant for complete data sovereignty
  - #### Integration with internal systems:
Connect to proprietary document management systems, knowledge bases, and internal financial analysis tools

### Data Source Expansion

  - #### Financial data providers:
Integrate with premium data sources like Bloomberg Terminal, Reuters Eikon, SIX Financial Information, or Refinitiv to enrich analysis with real-time market data
  - #### Regulatory filings:
Automate ingestion of EDGAR (SEC), ESMA, and other regulatory databases for comprehensive coverage of public disclosures
  - #### Analyst reports:
Incorporate research reports from various financial institutions to provide multiple perspectives on the same companies
  - #### News and sentiment analysis:
Add real-time news processing from financial news providers with sentiment analysis to track market perception

### Enhanced Analytics

  - Time-series visualization: Generate charts and graphs of financial metrics over time based on natural language requests
  - Comparative analysis: Enable side-by-side comparison of multiple companies or multiple reporting periods
  - Anomaly detection: Highlight unusual patterns or discrepancies in financial reporting
  - Financial ratio calculation: Automatically compute key financial ratios and benchmarks against industry standards
  - Currency normalization: Convert all financial figures to a single currency for consistent analysis

User Experience

  - Multi-language support: Extend capabilities to analyze reports in multiple languages and respond in the user's preferred language
  - Scheduled analysis: Set up recurring analysis of new reports as they become available
  - Customizable alerts: Configure notifications for specific financial events or thresholds
  - Collaborative features: Enable sharing of analyses, custom question templates, and annotations between team members

These enhancements would transform this prototype into an enterprise-grade solution that could significantly improve efficiency and insight generation for financial professionals across investment management, corporate finance, and regulatory compliance domains.

## Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is under the MIT License - see the [LICENCE](https://github.com/oujbou/fin_reports_analysis_helper/blob/main/LICENCE.md) file for details.

## Deployment
To deploy this application on Streamlit Cloud:

  - Host the code on GitHub
  - Log in to https://share.streamlit.io
  - Deploy the application by pointing to the repository
  - Configure secrets (API keys) in the Streamlit Cloud interface

## Important Notes for Deployment
When deploying to Streamlit Cloud, you'll need to set up your API keys as secrets:

  - Go to your app settings in Streamlit Cloud
  - Navigate to the "Secrets" section
  - Add your keys in the following format:
```toml
OPENAI_API_KEY = "your_openai_api_key"
PINECONE_API_KEY = "your_pinecone_api_key"
PINECONE_ENVIRONMENT = "your_pinecone_environment"
```


## Contact

For any questions, contact oujlakhtarik@gmail.com



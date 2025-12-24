# ScholarsDock
A local-only, privacy-focused RAG (Retrieval-Augmented Generation) assistant that enables secure interaction with documents using Streamlit, Ollama, and FAISS.

## About
ScholarsDock is designed to provide a secure and efficient way to query and interact with various document formats completely offline. By leveraging the power of local LLMs via Ollama and efficient vector search with FAISS, it ensures that your sensitive data never leaves your machine. Users can upload PDFs, DOCX, or TXT files and ask questions to get accurate, context-aware responses, making it an ideal tool for researchers, students, and professionals handling private documents.

## Features
- **Local Execution**: Runs entirely on your local machine with no external API calls, ensuring maximum privacy.
- **Document Support**: Seamlessly processes PDF, DOCX, and TXT files.
- **Context-Aware Answers**: Uses RAG (Retrieval-Augmented Generation) to provide accurate answers based on document content.
- **Source Citations**: Every response includes references to the specific source documents and text chunks.
- **Strict Mode**: Toggleable option to force the AI to answer *only* based on the provided documents.
- **Persistent Storage**: Vector embeddings are saved locally, so you don't have to re-process documents every time.

## Requirements
To run this project, you need the following:

- **Python 3.10+** installed on your system.  
- **Ollama**: You must have [Ollama](https://ollama.com/) installed and running.  
- **LLM Model**: Pull the required model using the command: `ollama pull qwen2.5`  
- **Python Dependencies**:  
    - `streamlit`
    - `ollama`
    - `faiss-cpu`
    - `sentence-transformers`
    - `langchain-text-splitters`
    - `pypdf`
    - `python-docx`

## System Architecture
<img width="806" height="220" alt="image" src="https://github.com/user-attachments/assets/f9e95a1e-0c48-406d-9459-531fed053ff8" />

## Output
<!--Embed the Output picture at respective places as shown below as shown below-->

### Output 1 - Home Page
<img width="1163" height="749" alt="image" src="https://github.com/user-attachments/assets/8ff31be4-748f-45fb-8f30-29a2f84739e0" />

### Output 2 - Document only Answer
<img width="1658" height="676" alt="image" src="https://github.com/user-attachments/assets/47a2c542-4e7e-43df-89a8-e92bb447a96b" />

### Output 3 - Idea generation + Document Analysis
<img width="1268" height="575" alt="image" src="https://github.com/user-attachments/assets/224cb787-8149-4465-a03d-cc0fd3f6edf9" />

## Results
### Performance Results  
**Accuracy**  
- Responses were highly relevant to the uploaded documents.
- Hallucinations were minimized due to RAG architecture.

**Efficiency**  
- Fast similarity search using FAISS.
- Low latency response generation on local machines.

**Scalability**  
- Successfully handled multiple documents.
- Performance scaled with available hardware resources.

**Privacy**  
- All data remained on the local system.
- No external data transmission.

## References
[1]     K. Suryavanshi, N. Thikekar, R. Pawar and S. Ashtekar, "Implementation of RAG Based Question-Answering Application," 2025 International Conference on Data Science and Business Systems (ICDSBS), Chennai, India, 2025. 

[2]       V. Kamra, L. Gupta, D. Arora and A. K. Yadav, "Enhancing Document Retrieval Using AI and Graph-Based RAG Techniques," 2024 5th International Conference on Communication, Computing & Industry 6.0 (C2I6), Bengaluru, India, 2024.

[3]       S. Vakayil, D. S. Juliet, A. J and S. Vakayil, "RAG-Based LLM Chatbot Using Llama-2," 2024 7th International Conference on Devices, Circuits and Systems (ICDCS), Coimbatore, India, 2024. 

[4]	P. Joshi, A. Gupta, P. Kumar and M. Sisodia, "Robust Multi Model RAG Pipeline For Documents Containing Text, Table & Images," 2024 3rd International Conference on Applied Artificial Intelligence and Computing (ICAAIC), Salem, India, 2024.

[5]	B. Saha, U. Saha and M. Zubair Malik, "QuIM-RAG: Advancing Retrieval-Augmented Generation With Inverted Question Matching for Enhanced QA Performance," in IEEE Access, vol. 12.

[6]	K. Sawarkar, A. Mangal and S. R. Solanki, "Blended RAG: Improving RAG (Retriever-Augmented Generation) Accuracy with Semantic Search and Hybrid Query-Based Retrievers," 2024 IEEE 7th International Conference on Multimedia Information Processing and Retrieval (MIPR), San Jose, CA, USA.

[7]	Tufino, Eugenio. “NotebookLM: An LLM with RAG for active learning and collaborative tutoring.” 

[8]	R. Patil, A. Nikam, T. Lichade, R. Patel, D. Maheshwari and A. Rajguru, "Intelligent PDF Query System for Document Analysis," 2025 International Conference on Cognitive Computing in Engineering, Communications, Sciences and Biomedical Health Informatics (IC3ECSBHI), Greater Noida, India, 2025.

[9]	V. Perov and V. Golovkov, "Ethics Documents in the Field of AI. Concepts, Achievements and Problems," 2024 IEEE Ural-Siberian Conference on Biomedical Engineering, Radioelectronics and Information Technology (USBEREIT), Yekaterinburg, Russian Federation, 2024

[10]	R. K, P. Gupta, G. Suthar, K. S. Sidhu, R. Sarkar and P. Satyanarayana, "Natural Language Processing for AI-Powered Legal Document Analysis," 2025 International Conference on Computing Technologies & Data Communication (ICCTDC), HASSAN, India, 2025

[11]	A. Ramprasad and P. Sivakumar, "Context-Aware Summarization for PDF Documents using Large Language Models," 2024 International Conference on Expert Clouds and Applications (ICOECA), Bengaluru, India, 2024

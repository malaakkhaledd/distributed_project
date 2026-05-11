Distributed LLM Load Balancing System
Overview
This project implements a distributed computing system capable of handling 1000+ concurrent AI requests using asynchronous processing, load balancing, GPU worker simulation, and Retrieval-Augmented Generation (RAG).
The system simulates a scalable AI inference environment where requests are distributed dynamically across CPU and GPU worker nodes.
________________________________________
Features
•	Async distributed request processing
•	Round Robin scheduling
•	Least Connections scheduling
•	Load-aware routing
•	CPU and GPU worker simulation
•	FLAN-T5 LLM integration
•	FAISS vector database
•	RAG pipeline
•	Fault tolerance support
•	Monitoring and latency tracking
•	1000 concurrent request simulation
________________________________________
Technologies Used
•	Python 3.10+
•	asyncio
•	HuggingFace Transformers
•	FAISS
•	PyTorch
•	NumPy
________________________________________
Project Structure
client/         -> request generation
common/         -> shared models
lb/             -> load balancer
llm/            -> FLAN-T5 inference
master/         -> scheduler/master node
rag/            -> retrieval pipeline
utils/          -> monitoring and fault tolerance
vector_db/      -> FAISS vector database
workers/        -> CPU/GPU workers
main.py         -> system entry point
________________________________________
Installation
Clone Repository
git clone <repository-link>
cd distributed_project
________________________________________
Install Dependencies
pip install -r requirements.txt
________________________________________
Required Libraries
pip install transformers torch faiss-cpu sentence-transformers numpy
________________________________________
Run the Project
python main.py
________________________________________
System Workflow
1.	Client generates requests
2.	Load balancer selects workers
3.	Workers retrieve RAG context
4.	FLAN-T5 generates responses
5.	Monitoring tracks statistics
6.	Responses returned to users
________________________________________
Performance Metrics
Example execution:
•	Total Requests: 1000
•	Successful Requests: 1000
•	Failed Requests: 0
•	Avg Latency: ~2.33 sec
•	Throughput: ~2.14 req/sec
________________________________________
Fault Tolerance
The system supports:
•	Worker failure detection
•	Request reassignment
•	Continuous request processing
________________________________________
Future Improvements
•	Real GPU cluster deployment
•	Docker/Kubernetes integration
•	Cloud deployment
•	Advanced scheduling algorithms
•	Larger LLM models


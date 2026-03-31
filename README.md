#  Enterprise-Grade Agentic RAG System
> A professional 3-tier AI application featuring autonomous routing, self-correcting retrieval, and automated cloud deployment.

![Build Status](https://img.shields.io/github/actions/workflow/status/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/backend-api-test.yml?branch=main&label=Backend%20CI)
![Docker Build](https://img.shields.io/github/actions/workflow/status/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/docker-publish.yml?branch=main&label=Docker%20Publish)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

##  System Architecture
This project implements a **3-tier architecture** designed for high scalability and production-grade reliability.

### High-Level Design (Mermaid Diagram)
```mermaid
graph TD
    User((User/Browser)) -->|React + Tailwind| Tier1[Frontend Tier]
    Tier1 -->|REST API| Tier2[Backend Tier: FastAPI]
    
    subgraph "Tier 2: The Agentic Brain"
    Tier2 -->|Invoke| LangGraph[LangGraph Orchestrator]
    LangGraph --> Router{Agentic Router}
    Router -->|Decision: RAG| Pinecone[Pinecone Vector DB]
    Router -->|Decision: Search| Tavily[Tavily Search API]
    
    LangGraph --> Grader{Retrieval Grader}
    Grader -->|Relevant| Generator[Groq Llama-3.3]
    Grader -->|Irrelevant| Tavily
    
    Generator -->|Hallucination Check| HallucinationGrader{Grader}
    end
    
    Tier2 -->|Nginx| AWS[AWS EC2 Cloud]
    GitHub[GitHub Actions] -->|CI/CD| AWS

# 🌟 Agentic RAG System (Production-Ready)

A fully production-ready **Agentic RAG (Retrieval-Augmented Generation)** system that intelligently routes queries between internal knowledge and real-time web data, with strong DevOps practices and scalable architecture.

---

## 🚀 Key Features

### 🧠 Autonomous Routing

* LLM-powered router decides dynamically:

  * 📚 Internal knowledge (Pinecone)
  * 🌐 Real-time web search (Tavily)

### 🔄 Self-Correcting Retrieval

* Built-in **grading system**:

  * Filters irrelevant documents
  * Automatically retries with better sources

### 🔗 Source Traceability

* Every answer includes:

  * Clickable references
  * Transparent source attribution

### 🏗️ Enterprise DevOps

* Multi-stage Docker builds
* Automated test pipelines
* Continuous Deployment to AWS

---

## 🛠️ Tech Stack

| Layer          | Technology                                                          |
| -------------- | ------------------------------------------------------------------- |
| **Frontend**   | React (Vite), Tailwind CSS, Lucide Icons, Axios                     |
| **Backend**    | FastAPI, Pydantic, Uvicorn, Python 3.11                             |
| **AI Brain**   | LangChain, LangGraph (State Machine), Groq (Llama-3.3)              |
| **Data Layer** | Pinecone (Vector DB), Tavily (Search API), HuggingFace (Embeddings) |
| **DevOps**     | Docker, Docker Compose, GitHub Actions, Nginx                       |
| **Cloud**      | AWS EC2 (t3.micro), Ubuntu 24.04                                    |

---

## 📂 Project Structure

```
.
├── .github/workflows/      # CI/CD pipelines
│
├── Backend/
│   ├── app/
│   │   ├── agent/          # LangGraph logic (nodes, chains, state)
│   │   ├── api/            # API routes (v1)
│   │   └── core/           # Config & settings (Pydantic)
│   │
│   ├── tests/              # Pytest suite (integration tests)
│   └── Dockerfile          # Backend container
│
├── frontend/
│   ├── src/                # React app
│   └── Dockerfile          # Nginx multi-stage build
│
└── docker-compose.yml      # Full stack orchestration
```

---

## ⚙️ Getting Started

### 🖥️ Local Development (No Docker)

#### 1. Backend Setup

```bash
cd Backend
pip install -r requirements.txt
python -m app.main
```

#### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

### 🐳 Production (Docker)

Run the entire system:

```bash
docker-compose up --build
```

👉 App will be live at:
**http://localhost**

---

## 🛡️ DevOps & CI/CD Pipeline

This project follows a **Zero-Trust Deployment Strategy**:

* ✅ **RAG Logic Tests**
  Validates agent routing & reasoning

* ✅ **Backend API Tests**
  Ensures endpoints and schemas work correctly

* ✅ **Docker Build Verification**
  Confirms containers build successfully

* ✅ **Smoke Tests**
  Runs full 3-tier system to verify integration

* ✅ **AWS Deployment**
  Auto-deploy to EC2 via SSH after passing all checks

---

## ☁️ Deployment Architecture

* AWS EC2 (t3.micro)
* Ubuntu 24.04
* Dockerized services
* Nginx as reverse proxy
* Swap memory optimization

---

## 👤 Author

**Enes Demir**

* GitHub: *your-github-link*
* LinkedIn: *your-linkedin-link*
* Live Project: *your-aws-ip-link*


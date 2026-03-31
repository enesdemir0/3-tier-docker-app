# 🚀 Enterprise-Grade Agentic RAG System
> A professional 3-tier AI application featuring autonomous routing, self-correcting retrieval, and automated cloud deployment.

![Build Status](https://img.shields.io/github/actions/workflow/status/enesdemir0/3-tier-docker-app/backend-api-test.yml?branch=main&label=Backend%20CI)
![Docker Build](https://img.shields.io/github/actions/workflow/status/enesdemir0/3-tier-docker-app/docker-publish.yml?branch=main&label=Docker%20Publish)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🏗️ System Architecture
This project implements a **3-tier architecture** designed for high scalability, security, and production-grade reliability.

### High-Level Design (Mermaid Flow)
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

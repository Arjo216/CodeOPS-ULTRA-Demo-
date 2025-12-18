🤖 CodeOps ULTRA: Demo Lite
A Proof-of-Concept Autonomous AI Agent for Rapid Code Generation and Verification.

📝 Project Overview
This is the Lite/Demo version of CodeOps ULTRA. It was built as a proof-of-concept to demonstrate the feasibility of an AI agent that can not only write code but also reason through logic errors.

This version served as the architectural foundation for the later CodeOps ULTRA Enterprise Edition, focusing on the core "Agentic Loop": Instruction → Generation → Reflection.

⚡ Core Features
Autonomous Coding: Leverages LLMs to interpret natural language and generate runnable Python code.

Simple Agentic Loop: Implements a basic feedback mechanism to detect and fix syntax errors.

Web Interface: A streamlined, user-friendly UI for interacting with the AI.

Dynamic Context: Support for basic file context to inform the agent's responses.

🛠️ Tech Stack
Frontend: React (Vite) / Tailwind CSS.

Backend: Python FastAPI.

AI: Google Gemini API.

Orchestration: LangChain / Basic State Management.

🚀 Setup Instructions
Prerequisites
Python 3.10+

Node.js & npm

Google Gemini API Key

Installation
Clone the Repo

git clone [https://github.com/Arjo216/CodeOPS-ULTRA-Demo.git](https://github.com/Arjo216/CodeOPS-ULTRA-Demo.git)
cd codeops-ultra-demo

Environment Configuration Create a .env file in the root directory:

GOOGLE_API_KEY=your_api_key_here

Backend Setup

cd backend
pip install -r requirements.txt
python main.py

Frontend Setup

cd frontend
npm install
npm run dev

⚠️ Disclaimer
This is a Lite Version and is intended for demonstration purposes only. Unlike the Enterprise version, this PoC:

Runs code in a local environment (no Docker sandboxing).

Does not include persistent database logging.

Lacks multimodal RAG (PDF/Image analysis).

Developed by Arjo216

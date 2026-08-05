# Autonomous Cloud Security Agent (DevSecOps)

Welcome to the **Autonomous Cloud Security Agent** project! This repository contains a DevSecOps AI Engine designed to autonomously analyze security alerts, investigate infrastructure configurations, and provide remediation steps or critical notifications based on cloud infrastructure events.

## 🚀 Project Overview

The core goal of this project is to integrate an autonomous AI agent into a DevSecOps pipeline. When a security alert is triggered (e.g., via AWS webhook), the backend processes this alert, uses Google's Gemini LLM along with LangChain tools to investigate the configuration (like checking Security Group rules for exposed ports), and acts accordingly.

## 🛠 Tech Stack & Frameworks

This project adopts a modern stack separated into a robust API backend and a reactive frontend.

### Backend
- **FastAPI (Python)**: Chosen for its high performance, automatic interactive API documentation, and asynchronous capabilities. It efficiently handles incoming webhooks and serves the API for the frontend.
- **LangChain**: A framework designed to simplify the creation of applications using large language models. It is used here to bind custom python tools (like AWS SDK mock checks) to the LLM.
- **Google Generative AI (Gemini Flash)**: The intelligence engine of the agent. Chosen for its fast reasoning, large context window, and excellent tool-calling capabilities.
- **Pydantic**: Used for robust data validation of incoming webhook payloads.

### Frontend
- **React**: A component-based JavaScript library for building interactive user interfaces.
- **Vite**: A lightning-fast build tool and development server, significantly improving the frontend development experience compared to older bundlers like Webpack.
- **Tailwind CSS**: A utility-first CSS framework chosen for rapid UI development and maintaining a consistent design system without writing custom CSS files.

---

## 💻 How to Run the Application

To run the application locally, you will need to start both the backend server and the frontend development server.

### 1. Backend Setup

1. **Navigate to the project root**:
   ```bash
   cd "devSecOps agent"
   ```

2. **Activate the virtual environment**:
   *Note: An environment named `.venv` already exists in this project.*
   ```bash
   # On macOS/Linux
   source .venv/bin/activate
   # On Windows
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies** (if not already installed):
   Ensure you have the required packages installed:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory (you can copy from `.env.example`) and add your Gemini API key:
   ```env
   GOOGLE_API_KEY="your_google_genai_api_key_here"
   ```

5. **Run the FastAPI Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will start at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node modules**:
   ```bash
   npm install
   ```

3. **Run the Vite Development Server**:
   ```bash
   npm run dev
   ```
   The frontend will start typically at `http://localhost:5173`.

---

## 🧠 Architecture Flow

1. A cloud provider (e.g., AWS) triggers a webhook to `POST /webhook/aws-alert`.
2. **FastAPI** receives the payload and passes it to the **LangChain** agent.
3. The **Gemini LLM** analyzes the prompt, determines that it needs more information, and calls the bound Python tool (e.g., `check_security_group_port`).
4. The tool executes (mocked AWS Boto3 logic) and returns the result to the LLM.
5. The LLM generates the final response/remediation which can be displayed on the React frontend.

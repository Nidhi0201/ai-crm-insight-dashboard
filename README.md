# AI CRM Insight Dashboard

A full‑stack, AI‑powered CRM dashboard that leverages machine learning to provide intelligent insights into customer behavior.  
It combines real‑time analytics, customer management, and predictive modeling to help teams make data‑driven decisions.

---

## ✨ Overview

The **AI CRM Insight Dashboard** is designed to answer questions like:

- Which customers are most likely to churn?
- Which segments respond best to a specific campaign?
- How are key metrics trending over time?

It provides:

- A React‑based analytics UI  
- A FastAPI backend for data and ML inference  
- Machine learning models (via scikit‑learn) for predictions  
- Cloud‑ready configuration for deployment (e.g., Render)

---

## 🧩 Features

- 📊 **Interactive dashboards**
  - Charts for KPIs like conversions, churn risk, engagement, etc.
  - Filters for segments, time ranges, and customer attributes

- 🤖 **ML‑powered insights**
  - scikit‑learn models for prediction and scoring
  - Churn/propensity scores surfaced directly in the UI

- 👥 **Customer management**
  - Customer profiles and attributes
  - Segmentation and tagging capabilities

- ⚙️ **FastAPI backend**
  - REST API endpoints for data, analytics, and predictions
  - Clean separation between API, data, and ML logic

- 🌐 **Cloud‑ready**
  - Designed for deployment on platforms like **Render**
  - Environment‑based configuration for API URLs and secrets

---

## 🛠 Tech Stack

| Layer          | Technology                         |
|----------------|------------------------------------|
| **Frontend**   | React, JavaScript/TypeScript       |
| **Backend**    | FastAPI (Python)                   |
| **ML / Data**  | scikit‑learn, Python data tooling  |
| **Deployment** | Render (or similar cloud platform) |
| **Versioning** | Git & GitHub                       |

---

## 🚀 Getting Started (Local Development)

> These steps assume a typical structure with separate `backend` and `frontend` folders.  
> Adjust paths if your project layout is slightly different.

### Prerequisites

- Node.js **18+**
- npm or yarn
- Python **3.10+**
- `pip` and `venv` (or `conda`)

---

### 1. Clone the repository

git clone https://github.com/Nidhi0201/ai-crm-insight-dashboard.git
cd ai-crm-insight-dashboard---

### 2. Backend setup (FastAPI + ML)

cd backend

# (Optional) create & activate virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txtCreate a `.env` file in `backend/` with configuration such as:

ENV=local
MODEL_PATH=models/model.pkl
DATABASE_URL=sqlite:///./data.dbRun the backend:

uvicorn main:app --reload --port 8000The FastAPI server should now be available at:

http://localhost:8000---

### 3. Frontend setup (React)

cd ../frontend

# Install dependencies
npm installConfigure the API base URL (for example, in `.env`):

REACT_APP_API_BASE_URL=http://localhost:8000Run the frontend dev server:

npm run dev          # or: npm startThe dashboard should now be accessible at something like:

http://localhost:3000---

## 🧱 High‑Level Architecture

ai-crm-insight-dashboard/
├── backend/                 # FastAPI + ML services
│   ├── main.py              # FastAPI app entry point
│   ├── routers/             # API route modules (customers, insights, etc.)
│   ├── models/              # Pydantic / DB models
│   ├── ml/                  # scikit-learn models & pipelines
│   └── requirements.txt
└── frontend/                # React dashboard
    ├── src/
    │   ├── components/      # Reusable UI components
    │   ├── pages/           # Dashboard pages/views
    │   ├── hooks/           # Data fetching & state logic
    │   └── services/        # API client helpers
    └── package.json**Data Flow:**

1. Frontend calls FastAPI endpoints for metrics, customer lists, and predictions  
2. Backend loads data and ML models (scikit‑learn)  
3. Predictions/scores are computed and returned as JSON  
4. React renders charts, tables, and dashboards from the API responses  

---

## 🌐 Deployment (Render Example)

> Generic outline if you host on [Render](https://render.com) or a similar platform.

### Backend (FastAPI)

- **Service type:** Web Service  
- **Build command:**  
 
  pip install -r requirements.txt
  - **Start command:**  
 
  uvicorn main:app --host 0.0.0.0 --port 8000
  - **Environment variables:**  
  e.g. `MODEL_PATH`, `DATABASE_URL`, and any API keys

### Frontend (React)

- **Service type:** Static Site  
- **Build command:**  
 
  npm install && npm run build
  - **Publish directory:** `dist` or `build` (depending on your tooling)  
- **Environment variables:**  
  `REACT_APP_API_BASE_URL=https://<your-backend-host>`

---

## 📄 License

You can add your preferred license here, for example:

MIT License – feel free to learn from or extend this project.
Please provide attribution if you use it in your own work.---

## 🙌 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for a fast, modern backend  
- [React](https://react.dev/) for the interactive dashboard UI  
- [scikit‑learn](https://scikit-learn.org/) for ML models and pipelines  
- [Render](https://render.com/) (or your chosen host) for deployment infrastructure  

---

## 👤 Author

**Nidhi Prajapati**  
- GitHub: [@Nidhi0201](https://github.com/Nidhi0201)  
- Portfolio: [nidhiprajapati.dev](https://nidhiprajapati.dev)

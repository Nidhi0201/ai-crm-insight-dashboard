from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
import joblib
import io
import numpy as np

# --------------------------------------------------------
# Setup
# --------------------------------------------------------
app = FastAPI(title="AI CRM Insight Dashboard", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for simplicity
STATE = {"df": None, "target": "churn", "model": None, "auc": None}


# --------------------------------------------------------
# Config models
# --------------------------------------------------------
class TrainConfig(BaseModel):
    target: str = "churn"
    id_column: str | None = "customer_id"


class ScoreConfig(BaseModel):
    threshold: float = 0.5


# --------------------------------------------------------
# Routes
# --------------------------------------------------------
@app.get("/")
def root():
    return {"ok": True, "message": "AI CRM Insight Dashboard API"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file")

    data = await file.read()
    df = pd.read_csv(io.BytesIO(data))

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV is empty")

    STATE["df"] = df
    return {"ok": True, "rows": len(df), "columns": list(df.columns)}


@app.post("/train")
async def train(cfg: TrainConfig):
    df = STATE["df"]
    if df is None:
        raise HTTPException(status_code=400, detail="No data uploaded")

    if cfg.target not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target '{cfg.target}' not found")

    y = df[cfg.target]
    drop_cols = [cfg.target]
    if cfg.id_column and cfg.id_column in df.columns:
        drop_cols.append(cfg.id_column)
    X = df.drop(columns=drop_cols)

    cat = [c for c in X.columns if X[c].dtype == "object"]
    num = [c for c in X.columns if c not in cat]

    pre = ColumnTransformer(
        [
            ("num", StandardScaler(with_mean=False), num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
        ]
    )

    model = Pipeline(
        [
            ("pre", pre),
            ("lr", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(X, y)
    proba = model.predict_proba(X)[:, 1]
    try:
        auc = float(roc_auc_score(y, proba))
    except Exception:
        auc = None

    STATE.update({"target": cfg.target, "model": model, "auc": auc})
    joblib.dump(model, "model.joblib")

    return {
        "ok": True,
        "auc": auc,
        "n_rows": int(len(X)),
        "n_features": int(X.shape[1]),
    }


@app.get("/metrics")
async def metrics():
    if STATE["df"] is None or STATE["model"] is None:
        raise HTTPException(status_code=400, detail="Need upload + train first")

    df = STATE["df"]
    target = STATE["target"]

    churn_rate = float(
        (df[target] == 1).mean() if df[target].dtype == "O" else df[target].mean()
    )

    pre = STATE["model"].named_steps["pre"]
    lr = STATE["model"].named_steps["lr"]

    num_cols = pre.transformers_[0][2]
    cat_enc: OneHotEncoder = pre.transformers_[1][1]
    cat_cols = pre.transformers_[1][2]
    cat_names = list(cat_enc.get_feature_names_out(cat_cols)) if len(cat_cols) else []
    feature_names = list(num_cols) + cat_names

    coef = lr.coef_.ravel()
    top_idx = np.argsort(np.abs(coef))[::-1][:10]
    top_features = [
        {"name": feature_names[i], "weight": float(coef[i])} for i in top_idx
    ]

    return {
        "ok": True,
        "auc": STATE["auc"],
        "churn_rate": churn_rate,
        "top_features": top_features,
    }


@app.post("/score")
async def score(_: ScoreConfig):
    if STATE["df"] is None or STATE["model"] is None:
        raise HTTPException(status_code=400, detail="Need upload + train first")

    df = STATE["df"]
    X = df.drop(
        columns=[STATE["target"]]
        + (["customer_id"] if "customer_id" in df.columns else [])
    )
    proba = STATE["model"].predict_proba(X)[:, 1]

    def rec(p):
        if p >= 0.8:
            return "Immediate outreach with retention offer"
        if p >= 0.6:
            return "Personalized email + schedule call"
        if p >= 0.4:
            return "Nurture campaign for engagement"
        return "Standard follow-up cadence"

    out = []
    for i, p in enumerate(proba):
        row = {"index": int(i), "prob": float(p), "recommendation": rec(float(p))}
        if "customer_id" in df.columns:
            row["customer_id"] = str(df.iloc[i]["customer_id"])
        out.append(row)

    return {"ok": True, "scores": out}


# --------------------------------------------------------
# Run manually for local testing
# --------------------------------------------------------
# Run using: uvicorn main:app --reload --port 8000

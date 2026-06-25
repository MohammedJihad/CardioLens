# CardioLens educational API — serves the FROZEN model. No training at runtime.
FROM python:3.12-slim
WORKDIR /app

# System libs scikit-learn / numpy need at runtime
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install only the slim API deps first (better layer caching)
COPY api/requirements.txt ./api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy the project (model, src, raw data, reports, config)
COPY . .

# Regenerate the processed dataset the explanation step reads at runtime
# (data/processed/*.csv is gitignored; data/raw/heart_cleveland.csv is committed)
RUN python -m src.data

# Most hosts inject $PORT (Render/Railway/Fly). HF Spaces expects 7860 — set PORT there.
ENV PORT=8000
EXPOSE 8000
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT}


# 🧠 GenAI Entity Extraction Pipeline

## Overview

This project is a modular, real-time pipeline designed to extract structured information — specifically **person names** and **dates** — from unstructured text using **Generative AI** and **Natural Language Processing** techniques. It combines the power of **Hugging Face Transformers**, **regex-based heuristics**, and **date normalization** to deliver clean, queryable data through a lightweight API.

---

## 🔧 Key Features

- **Named Entity Recognition (NER)** using BERT-based models
- **Date normalization** with support for informal formats
- **Subword token merging** for clean person name extraction
- **Regex fallback** for enhanced date coverage
- **Real-time file monitoring** via `watchdog`
- **SQLite database** for persistent storage
- **RESTful API** built with Flask
- **Duplicate detection** to prevent redundant inserts

---

## 📁 Architecture

```
genai_pipeline/
├── watch_folder/           # Directory for incoming .txt files
├── app.py                  # Flask API server
├── file_watcher.py         # Watches folder and triggers extraction
├── entity_extractor.py     # NER + regex + normalization logic
├── db.py                   # SQLite DB setup and insert logic
├── results.db              # Auto-generated SQLite database
├── requirements.txt        # Python dependencies
```

---

## 🧠 How It Works

1. **File Monitoring**: `file_watcher.py` continuously watches the `watch_folder/` directory for new `.txt` files.
2. **Entity Extraction**: When a file is detected, its contents are passed to `entity_extractor.py`, which:
   - Uses Hugging Face’s `dslim/bert-base-NER` model to extract person names and dates.
   - Applies regex to capture informal or missed date formats.
   - Normalizes all dates to `YYYY-MM-DD` using `dateparser`.
   - Merges subword tokens to reconstruct full names.
   - Removes fragments and duplicates for clean output.
3. **Data Storage**: Cleaned data is inserted into `results.db` via `db.py`, with duplicate file checks.
4. **API Access**: `app.py` exposes the data at `http://127.0.0.1:5000/results` in JSON format.

---

## 🔐 Hugging Face Token

To access the NER model, a Hugging Face access token is required. Replace the placeholder in `entity_extractor.py`:

```python
HF_TOKEN = "your_huggingface_token_here"
```

Generate your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/genai_pipeline.git
cd genai_pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Ensure Python 3.8+ is installed.

---

## 🖥️ Running the Pipeline

### Start the file watcher

```bash
python file_watcher.py
```

### Start the Flask API

```bash
python app.py
```

### Access results

Visit:

```
http://127.0.0.1:5000/results
```

---

## 📄 Requirements

```
transformers
watchdog
flask
dateparser
```

---


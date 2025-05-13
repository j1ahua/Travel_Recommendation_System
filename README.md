# 🌍 Travel Recommendation System

This project uses **semantic search** and **unsupervised learning** to recommend travel destinations based on user preferences. By combining Sentence-BERT embeddings, FAISS similarity search, and KMeans clustering, the system helps surface locations that are most relevant based on natural language queries and metadata.

---

## 🔧 Setup Instructions

Follow these steps to recreate the environment and run the Jupyter notebook.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Travel_Recommendation_System
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate         # On Windows: .\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open the `.ipynb` file and run the cells from the beginning.

---

## 📦 Dependencies

These are the main Python libraries used in this project:

* `pandas` – data manipulation and analysis
* `numpy` – numerical computations
* `matplotlib` – data visualization
* `scikit-learn` – machine learning models (PCA, KMeans, etc.)
* `sentence-transformers` – semantic embeddings using BERT
* `faiss-cpu` – fast similarity search
* `joblib` – saving and loading models
* `re` – regex processing (Python standard library)

All dependencies are listed in `requirements.txt`.

> 💡 **Note**: If you're on a GPU-enabled machine, you can optionally install `faiss-gpu` instead of `faiss-cpu`.

---

## 📚 What I Learned

Through this project, I explored:

* How **semantic embeddings** represent user intent
* How to combine **text and structured data** for recommendations
* How to use **FAISS** for scalable similarity search
* How to apply **clustering and PCA** for exploratory analysis and visualization
* The importance of creating a **reproducible Python environment**

Working on this deepened my interest in **natural language processing**, and I’m now excited to explore more NLP techniques and applications in the future.

---

## ✅ Environment Reproducibility

To ensure anyone can run this notebook, all dependencies are captured in `requirements.txt`. If you're sharing this with others:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

You can also register your virtual environment as a Jupyter kernel:

```bash
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

---

## 🖼️ Optional Enhancements

Want to extend this project?

* Add a web interface with **Streamlit** or **Flask**
* Use **user profiles or travel history** to personalize recommendations
* Train your own embedding model for a specific domain

---

## 📁 Project Structure

```
Travel_Recommendation_System/
├── data/                    # Dataset and metadata (optional)
├── venv/                    # Virtual environment (not tracked in Git)
├── notebook.ipynb           # Jupyter notebook with code
├── requirements.txt         # All required Python libraries
└── README.md                # Project overview and setup guide
```

---

## 📬 Contact

Feel free to reach out if you want to collaborate or chat about NLP, data science, or travel-tech ideas!


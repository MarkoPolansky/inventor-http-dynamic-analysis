# Installation Manual — eTLD+1 Clustering Analysis Notebook

## Prerequisites

| Requirement | Minimum version |
|---|-----------------|
| Python | 3.12+           |
| pip | 23+             | 


The analysis was developed and tested on Windows 11. 


## Optional Prerequisites
The following prerequisites are only required if you want to generate or update adblock filter cache yourself using a custom filter list.
For a detailed description see [`shared/README.md`](../../shared/README.md).

| Requirement | Minimum version |
|---|-----------------|
| Node.js | 18 LTS          | 
| npm | 9+              | 

> **Note:** The repository already includes a pre-populated adblock cache, so Node.js and npm are not required for normal installation and usage.

---

## 1. Clone / Obtain the Project

```bash
git clone <repository-url>
cd <project-root>
```

The expected top-level structure after cloning:

```
analysis_etl_plus_one_clustering/
analysis_single_resources/
analysis_time_series_EWMA/
data/
shared/
```

---

## 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows PowerShell
```

---

## 3. Install Python Dependencies

```bash
pip install -r analysis_etl_plus_one_clustering/requirements.txt
```

The `requirements.txt` covers all packages used in the notebook. Key dependencies include:

| Package | Purpose |
|---|---|
| `jupyter` / `jupyterlab` | Notebook runtime |
| `ipywidgets` | Interactive date slider and site selector |
| `tldextract` | eTLD+1 extraction from URLs |
| `matplotlib` | Chart rendering |
| `seaborn` | Heatmap rendering |
| `numpy` | Array operations for sliding-window detection |

If `ipywidgets` is installed but widgets do not render, enable the extension:

```bash
jupyter nbextension enable --py widgetsnbextension   # classic Notebook
# or for JupyterLab:
pip install jupyterlab-widgets
```


---

## 5. Download Raw Data Set

See [`data/README.md`](../../data/README.md).


## 6. Launch the Notebook

From the project root with the virtual environment active:

```bash
jupyter notebook
# or
jupyter lab
```

Navigate to `analysis_etl_plus_one_clustering/analysis_etdl_plus_one_clustering.ipynb` and run all cells from top to bottom.

---

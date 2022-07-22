# 🪐 MITRE ATT&CK Text Classification
This project extracts the MITRE ATT&CK technique, under a specific tactic, from a piece of cyber article. The tactic chosen for training and testing is Initial Access. Refer to https://attack.mitre.org/ for other possible tactics to train on.

## ✔️ Requirements 
1. Create a fresh conda environment in directory via `conda create -n <environment name> python=3.10.4 -y`.  
2. Activate the environment via `conda activate <environment name>`.  
3. Install packages via `pip install -r requirements.txt`.
4. Install spacy-transformers via `pip install -U scikit-learn`.

## ⏭ Components
This describes the workflow of the scripts and the assets used.

### 📋 Scripts
| File | Workflow | Description |
| --- | --- | --- |
| [`webscraper.py`](scripts/webscraper.py) | 1 | Scrapes MITRE ATT&CK specified techniques and their examples |
| [`paddingscraper.py`](scripts/paddingscraper.py) | 2 | Padding the training data with data from [`padding_data.tsv`](assets/padding_data.tsv) |
| [`paragraph_scraper_tester.py`](scripts/paragraph_scraper_tester.py) | 3 | Extracts paragraphs from [`annotations_20220531.json`](assets/annotations_20220531.json) to predict and compare results |

### 🗂 Assets
| File | Source | Description |
| --- | --- | --- |
| [`assets/annotations_20220531.json`](assets/annotations_20220531.json) | Local | Contains paragraphs and their generated Techniques |
| [`assets/training.csv`](assets/training.csv) | Local | Training data for model |
| [`assets/training_no_techn.csv`](assets/training_no_techn.csv) | Local | To train "No Technique Found" |
| [`assets/predicted.csv`](assets/predicted.csv) | Local | Collating the predicted results on  and their validity |
| [`model/model_best.pkl`](model/model_best.pkl) | Local | Trained multi-class text-classification model |

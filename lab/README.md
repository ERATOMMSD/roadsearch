# Experimental results

## Folder structure

```
.
+-- lab
| +-- data/ (requires downloading files)
| |   simulations/ folder containing 
| |   ...
| +-- figures/ figures produced by the notebooks that are displayed in the paper
| |   ...
| +-- src/ contains scripts to generate the data used in the noteboks from ../data/simulations/
| |  ...
+-- failures_detection.ipynb: analysis over failures
+-- search_diversity.ipynb: diversity of the search 
+-- alteration_diversity.ipynb: diversity of the alteration operator
+-- crossover_diversity.ipynb: diversity of the crossover operator
```

## Installation

It is suggested creating a virtual environment. 

```
python3 -m venv /path/to/new/virtual/environment
```

Then, activate the environment. 

```
source /path/to/new/virtual/environment/bin/activate
```

Install the requirements.

```
pip install -r requirements.txt
```

Launch jupyter lab to see the notebooks. 
```
jupyter lab
```

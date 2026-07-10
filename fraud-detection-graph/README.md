## Fraud Detection with Graph Theory Features inspired by my masters thesis

Detecting fraudulent financial transactions using classical ML and graph theory based features derivedd from transaction networks.

## Motivation
Fraud detection is a natural application of graph theory transacations form networks where fraudulent behaviour creates detectable structural patterns.

## Project Structure
- `notebooks/` step by step analysis
- `src/` reusable utility functions
- `data/` raw and processed datasets (not tracked in Git)
- `reports/` figures and findings

## Tech Stack
Python, Pandas, Scikit-learn, NetworkX, Matplotlib

## Status
🚧 In Progress


## Key Findings So Far

- Dataset: 1.3M transactions, 23 features
- Fraud rate: 0.58% — severely imbalanced dataset
- Fraudulent transactions skew higher in amount than legitimate ones
- Top fraud categories: grocery_pos (23%), shopping_net (23%), misc_net (12%)
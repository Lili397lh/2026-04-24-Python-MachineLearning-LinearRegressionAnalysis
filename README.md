# Linear Regression App

A desktop Python application for performing linear regression from a CSV file. It allows the user to load a dataset, view its contents, select the X and Y variables, apply an optional filter, and display both the scatter plot with the regression line and the main statistical results [file:1].

## Technologies and Libraries

This project is developed in **Python** and mainly uses the following libraries:

- `tkinter` for the graphical user interface.
- `matplotlib` to generate the chart.
- `pandas` to load and manipulate CSV data.
- `scikit-learn` or an equivalent custom implementation for linear regression, depending on the final code structure.

## Setup & Execution

1. Prerequisites:
- Python 3.10 or later is recommended.

2. Download Dataset:
- A CSV file with:
  - Comma-separated values.
  - Column names in the first row.
  - Valid numeric columns for regression.
- Or as example can be downloaded the next CSV from Kaggle:
  - https://www.kaggle.com/datasets/vipullrathod/fish-market

3. Run:
  1. Execute `main.py`
  2. Click in button `Select CSV` and select the CSV file
  3. Select variable X and Y
  4. Select a filter (Optional)
  5. Click in button `calculate`

## Author

Liliana Lain Huditian - Data Analyst.
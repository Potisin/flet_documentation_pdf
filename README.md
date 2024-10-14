# Flet Documentation PDF Generator

This project provides a Python script that automates the process of downloading the Flet framework documentation and compiling it into a single PDF file. By utilizing Pyppeteer, the script renders each documentation page as a PDF and then merges them into one comprehensive document.

## Usage

### Update the Navigation HTML

Open the `script.py` file.

Replace the placeholder `'''[PASTE YOUR NAVIGATION HTML HERE]'''` with the actual HTML code of the Flet documentation navigation panel.

```python
html_nav = '''[PASTE YOUR NAVIGATION HTML HERE]'''
```

```
python main.py
```

The script will create a directory named pdf_pages containing PDF versions of each documentation page.
A merged PDF named Flet_Documentation.pdf will be generated in the project root directory.
## PDF Converter

A simple command-line tool to extract text from PDF files and save it as Markdown.

## Features

- Extract text from a single PDF or batch process a folder of PDFs.
- Formats output with Markdown headings (`# Filename`, `## Page n`).
- Multithreaded folder processing with optional progress bar (`tqdm`).

## Requirements

- Python 3.6 or higher
- PyPDF2
- tqdm (optional, for progress display)

## Installation

1. Clone this repository or download the `pdf-converter.py` script.
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install PyPDF2 tqdm
   ```

## Usage

Run the script and follow the interactive prompts:

```bash
python pdf-converter.py
```

- Choose **1** to process a single PDF: calls [`process_single_file`](pdf-converter.py).
- Choose **2** to process all `.pdf` files in a folder: calls [`process_folder`](pdf-converter.py) with multithreading and progress.
- Choose **3** to exit.

Extracted Markdown files are saved in a new subfolder (named after each PDF) beside the original PDF.

## Key Functions

- [`extract_text_from_pdf`](pdf-converter.py): Reads a PDF and returns Markdown-formatted text.
- [`save_markdown_to_file`](pdf-converter.py): Writes Markdown text to an output folder.
- [`process_single_file`](pdf-converter.py): Handles single-file conversion.
- [`process_folder`](pdf-converter.py): Handles batch conversion with `ThreadPoolExecutor` and optional `tqdm`.

## License

MIT License. Feel free to use and modify.

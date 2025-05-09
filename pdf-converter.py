"""
PDF Converter

A command-line utility to extract text from PDF files and save it as Markdown.
Supports single-file or folder-wide (multithreaded) processing with an optional tqdm progress bar.
"""

import os                              # For file path manipulations
import PyPDF2                          # For reading PDF documents
from concurrent.futures import ThreadPoolExecutor, as_completed
# For parallel processing of multiple PDFs

try:
    from tqdm import tqdm             # Optional progress bar
except ImportError:
    tqdm = None                       # Fallback if tqdm is not installed


def extract_text_from_pdf(pdf_path):
    """
    Read each page of the PDF at `pdf_path` and build a Markdown string:
    - Level-1 heading is the filename
    - Level-2 heading for each page
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            md_text = f"# {os.path.basename(pdf_path)}\n"
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    # Append a page heading and its text
                    md_text += f"\n\n## Page {i+1}\n\n{page_text.strip()}\n"
            return md_text
    except (OSError, RuntimeError) as e:
        print(f"Error reading {pdf_path}: {e}")
        return None


def save_markdown_to_file(text, output_folder, output_filename):
    """
    Ensure `output_folder` exists, then write `text` to
    `output_folder/output_filename` using UTF-8 encoding.
    """
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    try:
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(text)
    except (OSError, IOError) as e:
        print(f"Error writing to {output_path}: {e}")


def prompt_path(prompt):
    """
    Prompt the user for a non-empty path.
    Repeats until input is non-blank (but does not validate existence here).
    """
    while True:
        path = input(prompt).strip()
        if path:
            return path


def process_single_file():
    """
    Prompt for a single PDF file path, extract its text to Markdown,
    and save it in a same-directory subfolder named after the PDF.
    """
    pdf_path = prompt_path("Enter the path to the PDF file: ")
    if not os.path.isfile(pdf_path):
        print("Invalid file path. Please try again.")
        return

    text = extract_text_from_pdf(pdf_path)
    if not text:
        return

    base = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(os.path.dirname(pdf_path), base)
    save_markdown_to_file(text, output_folder, base + ".md")
    print("1 file processed.")


def process_pdf_file_in_folder(folder_path, filename):
    """
    Worker for ThreadPoolExecutor:
    Process one PDF inside `folder_path`, return True if conversion succeeds.
    """
    pdf_path = os.path.join(folder_path, filename)
    text = extract_text_from_pdf(pdf_path)
    if text:
        base = os.path.splitext(filename)[0]
        output_folder = os.path.join(folder_path, base)
        save_markdown_to_file(text, output_folder, base + ".md")
        return True
    return False


def process_folder():
    """
    Prompt for a folder path, then:
    - Collect all .pdf files
    - Optionally show a tqdm progress bar
    - Process each PDF in parallel, saving Markdown to a subfolder per file
    """
    folder_path = prompt_path("Enter the path to the folder: ")
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return

    pdf_files = [f for f in os.listdir(
        folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    total_files = len(pdf_files)
    processed_count = 0

    # Initialize progress tracking
    if tqdm:
        progress = tqdm(total=total_files, desc="Processing PDFs", unit="file")
    else:
        progress = None
        print(f"Processing {total_files} PDF files...")

    # Parallel processing pool
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_pdf_file_in_folder, folder_path, fname): fname
            for fname in pdf_files
        }
        for future in as_completed(futures):
            try:
                if future.result():
                    processed_count += 1
            except (OSError, RuntimeError, PyPDF2.errors.PdfReadError) as e:
                print(f"Error processing {futures[future]}: {e}")
            finally:
                if progress:
                    progress.update(1)

    if progress:
        progress.close()

    print(
        f"Completed processing. {processed_count} out of {total_files} files converted.")


def main():
    """
    Display a simple menu:
    1) Process one PDF
    2) Process all PDFs in a folder
    3) Exit
    Loop until the user chooses to exit.
    """
    while True:
        print("\nChoose an option:")
        print("1. Process a single PDF file")
        print("2. Process all PDF files in a folder")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == '1':
            process_single_file()
        elif choice == '2':
            process_folder()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Entry point for script execution
    main()

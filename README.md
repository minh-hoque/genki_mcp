# Genki MCP

## Project Overview

**genki-mcp** is a Python project that serves structured content from the "Genki I" Japanese textbook. It exposes chapter content and metadata via an MCP (Modular Command Platform) server, using pre-extracted text. The project is designed for language learners, educators, and developers interested in building tools or bots around the Genki textbook.

---

## Features

- **Chapter Structuring**: Organizes extracted text by textbook chapters, with metadata and page ranges.
- **MCP Server**: Exposes chapter content and metadata via an MCP server, enabling integration with bots, chat interfaces, or other tools.
- **Extensible Tools**: Provides MCP tools to list chapters and retrieve chapter content programmatically.
- **Jupyter Notebook (Optional)**: Includes a notebook for PDF parsing and OCR experimentation (requires Tesseract, only if you want to re-extract text).

---

## Directory Structure

```
.
├── main.py                  # Main entrypoint, runs the MCP server
├── pyproject.toml           # Project metadata and dependencies
├── .env                     # Environment variables (e.g., OpenAI API key)
├── data/
│   ├── Genki Textbook 2nd Edition.pdf   # Source textbook PDF (not included in repo)
│   └── pdf_images/          # (Likely) contains images of PDF pages
├── output/
│   └── extracted_text.json  # Extracted and OCR'd text, organized by page
├── notebooks/
│   └── scanned_pdf_parsing.ipynb # Jupyter notebook for PDF/OCR processing (optional)
└── README.md                # This file
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd genki_mcp
   ```

2. **Install [uv](https://github.com/astral-sh/uv):**
   - On macOS: `brew install uv`
   - On Ubuntu: `curl -Ls https://astral.sh/uv/install.sh | sh`

3. **Install dependencies with uv:**
   ```bash
   uv pip install -r pyproject.toml
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and add your OpenAI API key (required for some features).

---

## Usage

### 1. **Run the MCP Server**

The MCP server uses the already extracted text in `output/extracted_text.json`.

```bash
uv pip install -r pyproject.toml  # Ensure dependencies are installed
uv run main.py
```

- The server will load the extracted text and expose MCP tools for chapter retrieval and listing.

### 2. **Available MCP Tools**

- `get_genki_chapter(chapter_number: str)`: Retrieve structured text for a specific chapter.
- `list_genki_chapters()`: List all available chapters with metadata.

These tools can be called programmatically or integrated into bots and chat interfaces using the MCP framework.

---

## Optional: Extract Text from PDF (For Developers)

- If you want to re-extract text from the Genki PDF, use the Jupyter notebook `notebooks/scanned_pdf_parsing.ipynb`.
- **This step requires [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and is not needed for running the MCP server.**
- The output will be saved as `output/extracted_text.json`.
- You must provide your own copy of "Genki Textbook 2nd Edition.pdf" in the `data/` directory.

---

## Configuration

- **.env**: Store your OpenAI API key and other secrets here.
- **pyproject.toml**: Manage dependencies and project metadata.

---

## Dependencies

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- [mcp](https://pypi.org/project/mcp/) (Modular Command Platform)
- openai, httpx, ipykernel, pdf2image, pillow, pytesseract, python-dotenv
- **Tesseract OCR is only required if you want to use the notebook for re-extraction.**

All Python dependencies are listed in `pyproject.toml`.

---

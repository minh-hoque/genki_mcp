import os
import json
from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("genki")

print("✅ Starting Genki MCP server...")

# Load extracted text from previously saved JSON
EXTRACTED_TEXT_PATH = (
    "/Users/minhajulhoque/work/github/mcps/genki_mcp/output/extracted_text.json"
)

if os.path.exists(EXTRACTED_TEXT_PATH):
    with open(EXTRACTED_TEXT_PATH, "r", encoding="utf-8") as f:
        extracted_text = json.load(f)
else:
    raise FileNotFoundError(f"Missing file: {EXTRACTED_TEXT_PATH}")

# Metadata for each chapter in Genki textbook
GENKI_CHAPTERS = {
    "0": {
        "title": "Genki I - Chapter 0: Greetings & Expressions",
        "description": "Covers essential greetings, classroom expressions, and daily phrases.",
        "pages": [34, 37],
    },
    "1": {
        "title": "Genki I - Chapter 1: New Friends",
        "description": "Introduces self-introductions, time expressions, and basic sentence structure.",
        "pages": [38, 57],
    },
    "2": {
        "title": "Genki I - Chapter 2: Shopping",
        "description": "Introduces shopping phrases, demonstratives (これ/それ/あれ), and sentence-ending particles.",
        "pages": [58, 83],
    },
    "3": {
        "title": "Genki I - Chapter 3: Making a Date",
        "description": "Covers verb conjugation, verb types, time references, and word order.",
        "pages": [84, 101],
    },
    "4": {
        "title": "Genki I - Chapter 4: The First Date",
        "description": "Covers describing locations, past tense, and particles for quantity.",
        "pages": [102, 127],
    },
    "5": {
        "title": "Genki I - Chapter 5: A Trip to Okinawa",
        "description": "Covers adjectives, making suggestions, and counting.",
        "pages": [128, 145],
    },
    "6": {
        "title": "Genki I - Chapter 6: A Day in Robert's Life",
        "description": "Covers te-form usage, giving instructions, combining activities, and expressing reasons.",
        "pages": [146, 165],
    },
    "7": {
        "title": "Genki I - Chapter 7: Family Picture",
        "description": "Covers describing appearance, te-form for combining sentences, and counting people.",
        "pages": [166, 185],
    },
    "8": {
        "title": "Genki I - Chapter 8: Barbecue",
        "description": "Covers short forms, informal speech, expressing preferences, and conjunction particles.",
        "pages": [186, 207],
    },
    "9": {
        "title": "Genki I - Chapter 9: Kabuki",
        "description": "Covers past tense short forms, qualifying nouns with verbs/adjectives, and expressions like まだ〜ていません and 〜から.",
        "pages": [208, 227],
    },
    "10": {
        "title": "Genki I - Chapter 10: Winter Vacation Plans",
        "description": "Covers comparisons between two or more items, using 〜つもりだ, adjective + なる, and location expressions like どこかに.",
        "pages": [228, 249],
    },
    "11": {
        "title": "Genki I - Chapter 11: After the Vacation",
        "description": "Covers expressing desires with 〜たい, listing actions with 〜たり〜たりする, and expressing experiences with 〜ことがある.",
        "pages": [250, 265],
    },
    "12": {
        "title": "Genki I - Chapter 12: Feeling III",
        "description": "Covers explanatory 〜んです, excessiveness with 〜すぎる, advice with 〜ほうがいいです, reasons with 〜ので, and obligation expressions.",
        "pages": [266, None],
    },
}


# Add parsed/extracted text into GENKI_CHAPTERS
for chapter_id, chapter_info in GENKI_CHAPTERS.items():
    start_page, end_page = chapter_info["pages"]

    # If end_page is None (e.g., last chapter), treat as a single page
    if end_page is None:
        end_page = start_page

    # Collect text from extracted pages
    pages_text = []
    for page_num in range(start_page, end_page + 1):
        page_key = str(page_num)
        if page_key in extracted_text:
            pages_text.append(
                f"--- Page {page_num} ---\n{extracted_text[page_key]['text']}"
            )
        else:
            pages_text.append(f"--- Page {page_num} ---\n[Text not found]")

    # Join the pages and insert into chapter
    chapter_info["text"] = "\n\n".join(pages_text)

# --- MCP Tools ---


@mcp.tool()
async def get_genki_chapter(chapter_number: str) -> str:
    """Retrieve parsed and structured text from a Genki textbook chapter.

    Args:
        chapter_number: The chapter number as a string (e.g., "1", "2", ...)

    Returns:
        A string with the structured chapter title and text.
    """
    chapter = GENKI_CHAPTERS.get(chapter_number)
    if not chapter:
        return f"❌ Chapter {chapter_number} not found in the Genki textbook database."

    return f"{chapter['title']}\n\n{chapter['text']}"


@mcp.tool()
async def list_genki_chapters() -> str:
    """List all available Genki chapters with metadata.

    Returns:
        A string summary of all available chapters, including chapter number, title, description, and page range.
    """
    result = []
    for chapter_num, chapter in GENKI_CHAPTERS.items():
        start, end = chapter["pages"]
        page_range = f"{start} - {end}" if end else f"{start}"
        summary = f"""
Chapter {chapter_num}: {chapter['title']}
Description: {chapter['description']}
Pages: {page_range}
        """.strip()
        result.append(summary)

    return "\n\n---\n\n".join(result)


# --- Entrypoint ---
if __name__ == "__main__":
    print("🚀 MCP server running with stdio transport.")
    mcp.run(transport="stdio")
    print("🛑 MCP server has shut down.")

import os
import json
from typing import Any
from mcp.server.fastmcp import FastMCP
import mcp.types as types

# Initialize FastMCP server
mcp = FastMCP("genki")

print("✅ Starting Genki MCP server...")

# Load extracted text from previously saved JSON
CHAPTER_METADATA_PATH = "data/chapter_metadata.json"
PAGES_PATH = "data/pages.json"
LESSONS_PATH = "data/lessons.json"

# Load pages data
if os.path.exists(PAGES_PATH):
    with open(PAGES_PATH, "r", encoding="utf-8") as f:
        extracted_text = json.load(f)
else:
    raise FileNotFoundError(f"Missing file: {PAGES_PATH}")

# Load chapter metadata from JSON file
if os.path.exists(CHAPTER_METADATA_PATH):
    with open(CHAPTER_METADATA_PATH, "r", encoding="utf-8") as f:
        GENKI_CHAPTERS = json.load(f)
else:
    raise FileNotFoundError(f"Missing file: {CHAPTER_METADATA_PATH}")

# Load lessons data
if os.path.exists(LESSONS_PATH):
    with open(LESSONS_PATH, "r", encoding="utf-8") as f:
        GENKI_LESSONS = json.load(f)
else:
    raise FileNotFoundError(f"Missing file: {LESSONS_PATH}")

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

# Add parsed/extracted text into GENKI_LESSONS
for lesson_id, lesson_info in GENKI_LESSONS.items():
    start_page, end_page = lesson_info["pages"]
    # If end_page is None (e.g., last lesson), treat as a single page
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
    # Join the pages and insert into lesson
    lesson_info["text"] = "\n\n".join(pages_text)

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


@mcp.tool()
async def get_chapter_based_on_user_request(chapter_number: str) -> str:
    """
    Retrieve parsed and structured text from a Japanese lesson chapter based on the user's learning request.

    Use this tool whenever the user asks about learning a specific topic in Japanese. The following chapters and their topics are available:

    0: Genki I - Chapter 0: Greetings & Expressions
       - Essential greetings, classroom expressions, and daily phrases.
    1: Genki I - Chapter 1: New Friends
       - Self-introductions, time expressions, and basic sentence structure.
    2: Genki I - Chapter 2: Shopping
       - Shopping phrases, demonstratives (これ/それ/あれ), and sentence-ending particles.
    3: Genki I - Chapter 3: Making a Date
       - Verb conjugation, verb types, time references, and word order.
    4: Genki I - Chapter 4: The First Date
       - Describing locations, past tense, and particles for quantity.
    5: Genki I - Chapter 5: A Trip to Okinawa
       - Adjectives, making suggestions, and counting.
    6: Genki I - Chapter 6: A Day in Robert's Life
       - Te-form usage, giving instructions, combining activities, and expressing reasons.
    7: Genki I - Chapter 7: Family Picture
       - Describing appearance, te-form for combining sentences, and counting people.
    8: Genki I - Chapter 8: Barbecue
       - Short forms, informal speech, expressing preferences, and conjunction particles.
    9: Genki I - Chapter 9: Kabuki
       - Past tense short forms, qualifying nouns with verbs/adjectives, and expressions like まだ〜ていません and 〜から.
    10: Genki I - Chapter 10: Winter Vacation Plans
        - Comparisons between two or more items, using 〜つもりだ, adjective + なる, and location expressions like どこかに.
    11: Genki I - Chapter 11: After the Vacation
        - Expressing desires with 〜たい, listing actions with 〜たり〜たりする, and expressing experiences with 〜ことがある.
    12: Genki I - Chapter 12: Feeling III
        - Explanatory 〜んです, excessiveness with 〜すぎる, advice with 〜ほうがいいです, reasons with 〜ので, and obligation expressions.

    Pass the appropriate chapter_number (as a string) based on the user's request.

    Args:
        chapter_number: The chapter number as a string (e.g., "1", "2", ...)

    Returns:
        A string with the structured chapter title and text.
    """
    chapter = GENKI_CHAPTERS.get(chapter_number)
    if not chapter:
        return (
            f"❌ Chapter {chapter_number} not found in the Japanese lessons database."
        )

    return f"{chapter['title']}\n\n{chapter['text']}"


@mcp.tool()
async def get_genki_lesson(lesson_key: str) -> str:
    """Retrieve parsed and structured text from a specific Genki lesson in a chapter.

    Args:
        lesson_key: The lesson key as a string (e.g., 'chapter_1_lesson_2')

    Returns:
        A string with the structured lesson title, description, and text.
    """
    lesson = GENKI_LESSONS.get(lesson_key)
    if not lesson:
        return f"❌ Lesson {lesson_key} not found in the Genki lessons database."
    return f"{lesson['lesson_title']}\n\n{lesson['lesson_description']}\n\n{lesson['text']}"


@mcp.tool()
async def list_genki_lessons_for_chapter(chapter_idx: str) -> str:
    """List all lessons for a given chapter with metadata.

    Args:
        chapter_idx: The chapter index as a string (e.g., '1', '2', ...)

    Returns:
        A string summary of all lessons in the chapter, including lesson key, title, description, and page range.
    """
    lessons = [
        (lesson_key, lesson)
        for lesson_key, lesson in GENKI_LESSONS.items()
        if str(lesson.get("chapter_idx")) == chapter_idx
    ]
    if not lessons:
        return f"❌ No lessons found for chapter {chapter_idx}."
    result = []
    for lesson_key, lesson in lessons:
        start, end = lesson["pages"]
        page_range = f"{start} - {end}" if end != start else f"{start}"
        summary = f"""
            Lesson key: {lesson_key}
            Title: {lesson['lesson_title']}
            Description: {lesson['lesson_description']}
            Pages: {page_range}
                    """.strip()
        result.append(summary)
    return "\n\n---\n\n".join(result)


@mcp.tool()
async def list_genki_lessons() -> str:
    """List all available Genki lessons in all chapters with metadata.

    Returns:
        A string summary of all available lessons, including lesson key, title, description, and page range.
    """
    result = []
    for lesson_key, lesson in GENKI_LESSONS.items():
        start, end = lesson["pages"]
        page_range = f"{start} - {end}" if end != start else f"{start}"
        summary = f"""
            Lesson key: {lesson_key}
            Title: {lesson['lesson_title']}
            Description: {lesson['lesson_description']}
            Pages: {page_range}
                    """.strip()
        result.append(summary)
    total = len(GENKI_LESSONS)
    return f"Total lessons: {total}\n\n" + "\n\n---\n\n".join(result)


# --- MCP Prompt for Lesson Search (FastMCP style) ---
@mcp.prompt()
def find_relevant_lessons_prompt(query: str) -> list[types.PromptMessage]:
    """Given a user query, return a list of lesson_keys from the Genki lessons that are relevant to the user's request."""
    lesson_summaries = []
    for lesson_key, lesson in GENKI_LESSONS.items():
        lesson_summaries.append(
            f"{lesson_key}: {lesson['lesson_title']}\n{lesson['lesson_description']}"
        )
    lessons_blob = "\n\n".join(lesson_summaries)
    prompt_text = f"""
        You are an expert at mapping user learning requests to relevant Japanese lessons.

        Here are all available lessons from the Genki textbook, with their keys, titles, and descriptions:

        {lessons_blob}

        Given the following user query, return a Python list of the lesson_keys (e.g., ['chapter_1_lesson_2', ...]) that are most relevant to what the user is asking for. Only include lesson_keys that are a good match. If none are relevant, return an empty list.

        User query: {query}
        lesson_keys: 
        """
    return [
        types.PromptMessage(
            role="user", content=types.TextContent(type="text", text=prompt_text)
        )
    ]


# --- Entrypoint ---
if __name__ == "__main__":
    print("🚀 MCP server running with stdio transport.")
    mcp.run(transport="stdio")
    print("🛑 MCP server has shut down.")

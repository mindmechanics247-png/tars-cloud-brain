import re

def clean_text(text: str) -> str:
    """
    Remove markdown, newlines and extra whitespace for safe display.
    """
    if text is None:
        return ""
    # convert bytes to str if needed
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8", errors="ignore")
        except:
            text = str(text)
    text = re.sub(r'[\r\n]+', ' ', str(text))
    text = re.sub(r'[*_`#>\[\]]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


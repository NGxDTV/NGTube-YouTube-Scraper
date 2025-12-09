import re


def extract_number(text):
    """
    Extract and parse numbers from text, handling German number formatting.

    Args:
        text (str): The text containing numbers.

    Returns:
        int: The extracted number.
    """
    if not text:
        return 0
    text = text.strip()
    multiplier = 1
    if 'Mio' in text:
        multiplier = 1000000
        text = text.replace('Mio.', '').replace('Mio', '').strip()
    elif 'M' in text and 'Mio' not in text:
        multiplier = 1000000
        text = text.replace('M', '').strip()
    elif 'K' in text:
        multiplier = 1000
        text = text.replace('K', '').strip()
    cleaned = re.sub(r'[^\d.,]', '', text)
    if '.' in cleaned and ',' not in cleaned:
        num_str = cleaned.replace('.', '')
    elif ',' in cleaned and '.' not in cleaned:
        num_str = cleaned.replace(',', '.')
    elif ',' in cleaned and '.' in cleaned:
        num_str = cleaned.replace('.', '').replace(',', '.')
    else:
        num_str = cleaned
    try:
        num = float(num_str)
        return int(num * multiplier)
    except Exception:
        return 0


def extract_links(text):
    """
    Extract URLs from text.

    Args:
        text (str): The text containing URLs.

    Returns:
        list: List of extracted URLs.
    """
    if not text:
        return []
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls
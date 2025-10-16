"""
CSV preprocessing for extracting search terms and creating action descriptions.
"""

import pandas as pd
import re
from urllib.parse import unquote


def extract_search_term_from_url(page_url):
    """Extract search term from URL parameters"""
    if not page_url or pd.isna(page_url):
        return ""
    page_url = str(page_url)

    # Common search parameter patterns across different sites
    # Patterns are AI Generated
    search_patterns = [
        r'searchTermRaw=([^&]+)',
        r'searchTerm=([^&]+)',
        r'[?&]q=([^&]+)',
        r'[?&]k=([^&]+)',
        r'[?&]st=([^&]+)',
        r'[?&]query=([^&]+)',
        r'[?&]search=([^&]+)',
        r'[?&]term=([^&]+)',
        r'[?&]keywords=([^&]+)',
    ]

    for pattern in search_patterns:
        match = re.search(pattern, page_url, re.IGNORECASE)
        if match:
            search_term = match.group(1)
            # URL decode the search term
            return unquote(search_term)

    return ""


def create_action_description(row):
    """Create a readable description for each action"""
    if row['type'] == 'click':
        if row['extracted_search_term']:
            return f"Clicked on '{row['click_text']}' (searching for: {row['extracted_search_term']})"
        else:
            return f"Clicked on '{row['click_text']}'"
    elif row['type'] == 'typing':
        if row['extracted_search_term']:
            return f"Typed text (likely searching for: {row['extracted_search_term']})"
        else:
            return "Typed text"
    elif row['type'] == 'scrolling':
        return "Scrolled the page"
    else:
        return f"Performed {row['type']} action"


def preprocess_csv(input_path, output_path):
    """Preprocess CSV to add search term extraction"""
    df = pd.read_csv(input_path)

    df['search_term_from_url'] = df['page_url'].apply(extract_search_term_from_url)
    df['extracted_search_term'] = ""

    # Checking if a click action was followed by typing
    # Used to extract search terms from URLs
    for i in range(len(df)):
        if df.iloc[i]['type'] == 'click':
            for j in range(i + 1, min(i + 6, len(df))):
                if df.iloc[j]['type'] == 'typing':
                    for k in range(i + 1, min(i + 6, len(df))):
                        search_term = extract_search_term_from_url(df.iloc[k]['page_url'])
                        if search_term:
                            df.iloc[i, df.columns.get_loc('extracted_search_term')] = search_term
                            break
                    break

    df['action_description'] = df.apply(create_action_description, axis=1)

    # Save processed data
    df.to_csv(output_path, index=False)

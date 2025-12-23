# agent/tools_search.py
"""
google_search.py
Provides a search tool used by the agent.
- Primary: Google Custom Search (GOOGLE_SEARCH_API_KEY + SEARCH_ENGINE_ID)
- Fallback: SerpAPI (SERPAPI_KEY)
Returns a concise JSON-friendly dict with title, snippet, link for top results.
"""

import os
import requests
from typing import List, Dict

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

def _google_cse_search(query: str, num: int = 3) -> List[Dict]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    items = data.get("items", [])[:num]
    results = []
    for it in items:
        results.append({
            "title": it.get("title"),
            "snippet": it.get("snippet"),
            "link": it.get("link")
        })
    return results

def _serpapi_search(query: str, num: int = 3) -> List[Dict]:
    url = "https://serpapi.com/search.json"
    params = {"q": query, "engine": "google", "num": num, "api_key": SERPAPI_KEY}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    res = []
    organic = data.get("organic_results") or data.get("organic_results", [])
    for o in organic[:num]:
        res.append({
            "title": o.get("title"),
            "snippet": o.get("snippet") or o.get("snippet_text") or "",
            "link": o.get("link") or o.get("displayed_link", "")
        })
    return res

def google_search(query: str, max_results: int = 3) -> Dict:
    """
    Search the web for `query`. Returns {"source": "google|serpapi", "results": [...]}
    Each result: {"title","snippet","link"}
    """
    if GOOGLE_SEARCH_API_KEY and SEARCH_ENGINE_ID:
        try:
            results = _google_cse_search(query, num=max_results)
            return {"source": "google_cse", "query": query, "results": results}
        except Exception as e:
            # fallback to SerpAPI if available
            pass

    if SERPAPI_KEY:
        try:
            results = _serpapi_search(query, num=max_results)
            return {"source": "serpapi", "query": query, "results": results}
        except Exception as e:
            pass

    # No search provider configured
    return {"source": "none", "query": query, "results": [], "error": "No search API configured"}

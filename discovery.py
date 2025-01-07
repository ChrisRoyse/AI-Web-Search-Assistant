"""
Search and caching functionality for the AI Web Search Assistant.
"""
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any
import requests
from datetime import datetime, timedelta
from duckduckgo_search import DDGS
import settings

class SearchDiscovery:
    def __init__(self):
        """Initialize the search discovery system."""
        self.bing_headers = {
            'Ocp-Apim-Subscription-Key': settings.BING_API_KEY
        }
        self.cache = {}
        self._clean_old_cache()

    def _clean_old_cache(self):
        """Remove cache files older than CACHE_MAX_AGE_DAYS."""
        current_time = datetime.now()
        for cache_file in settings.CACHE_DIR.glob('*.json'):
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if current_time - file_time > timedelta(days=settings.CACHE_MAX_AGE_DAYS):
                cache_file.unlink()

    def _get_cache_path(self, query: str) -> Path:
        """Generate a cache file path for a given query."""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return settings.CACHE_DIR / f"{query_hash}.json"

    def _load_cache(self, query: str) -> Dict[str, Any]:
        """Load cached results for a query if they exist."""
        cache_path = self._get_cache_path(query)
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self, query: str, data: Dict[str, Any]):
        """Save search results to cache."""
        cache_path = self._get_cache_path(query)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def search_bing(self, query: str) -> List[str]:
        """Perform a Bing search."""
        try:
            response = requests.get(
                settings.BING_ENDPOINT,
                headers=self.bing_headers,
                params={'q': query, 'count': settings.RESULTS_PER_SEARCH},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return [
                f"{result['name']}: {result['snippet']}"
                for result in data.get('webPages', {}).get('value', [])
            ]
        except Exception as e:
            print(f"Bing search error: {e}")
            return []

    def search_duckduckgo(self, query: str) -> List[str]:
        """Perform a DuckDuckGo search."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    max_results=settings.RESULTS_PER_SEARCH
                ))
                return [
                    f"{result['title']}: {result['body']}"
                    for result in results
                ]
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []

    def perform_search_round(self, query: str) -> List[str]:
        """Perform a single round of searching using both search engines."""
        # Check cache first
        cache_data = self._load_cache(query)
        if cache_data:
            return cache_data.get('results', [])

        # Perform new searches
        bing_results = self.search_bing(query)
        ddg_results = self.search_duckduckgo(query)
        
        # Combine and deduplicate results
        all_results = list(set(bing_results + ddg_results))
        
        # Cache the results
        self._save_cache(query, {
            'query': query,
            'timestamp': time.time(),
            'results': all_results
        })
        
        return all_results 
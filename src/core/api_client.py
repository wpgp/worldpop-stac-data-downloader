"""
STAC API Client for WorldPop Desktop App
"""
from typing import Dict, List, Optional, Any

import requests


class WorldPopSTACClient:
    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })

    def get_collections(self) -> List[Dict[str, Any]]:
        """Get all collections from STAC API"""
        try:
            response = self.session.get(f"{self.base_url}/collections")
            response.raise_for_status()
            return response.json().get("collections", [])
        except requests.RequestException as e:
            print(f"Error fetching collections: {e}")
            return []

    def get_collection(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """Get specific collection"""
        try:
            response = self.session.get(f"{self.base_url}/collections/{collection_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching collection {collection_id}: {e}")
            return None

    def search_items(self, collections: List[str] = None,
                     bbox: List[float] = None,
                     datetime: str = None,
                     query: Dict[str, Any] = None,
                     filter_expr: str = None,
                     filter_lang: str = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """Search for STAC items with filters"""
        search_params = {
            "limit": limit
        }

        if collections:
            search_params["collections"] = collections
        if bbox:
            search_params["bbox"] = bbox
        if datetime:
            search_params["datetime"] = datetime
        if query:
            search_params["query"] = query
        if filter_expr:
            search_params["filter"] = filter_expr
        if filter_lang:
            search_params["filter-lang"] = filter_lang

        # print(f"Search request: {search_params}")  # Debug output

        try:
            response = self.session.post(
                f"{self.base_url}/search",
                json=search_params
            )
            # print(f"Response status: {response.status_code}")
            # if response.status_code != 200:
            #     print(f"Response text: {response.text}")
            response.raise_for_status()
            return response.json().get("features", [])
        except requests.RequestException as e:
            print(f"Error searching items: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error response: {e.response.text}")
            return []

    def get_item(self, collection_id: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Get specific item"""
        try:
            response = self.session.get(
                f"{self.base_url}/collections/{collection_id}/items/{item_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching item {item_id}: {e}")
            return None

    def download_file(self, url: str, local_path: str, progress_callback=None) -> bool:
        """Download file from URL with progress callback"""
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback:
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            progress_callback(progress, downloaded, total_size)

            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

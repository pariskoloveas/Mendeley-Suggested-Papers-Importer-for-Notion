import os
import requests
import re
import json


class NotionService:
    BASE_API_URL = 'https://api.notion.com/v1/pages'

    def __init__(self):
        self.setup_settings()

    def setup_settings(self):
        self.api_key: str = os.getenv('NOTION_API_KEY')
        self.db_id: str = os.getenv('NOTION_DATABASE_ID')
        self.URL_HEADERS = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16"
        }

    def add_entries(self, entry):
        headers = self.URL_HEADERS
        # url = f'https://api.notion.com/v1/pages'
        payload = self.get_payload(entry)
        print(json.dumps(payload))
        # response = requests.request('PATCH', url, headers=headers, json=json.dumps(payload))
        response = requests.post(self.BASE_API_URL, headers=headers, data=json.dumps(payload))

        if not response.ok:
            raise NotionServiceException(response.json())

    def get_payload(self, entry):
        return {
            "parent": {
                "database_id": self.db_id
            },
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": entry[0]
                            }
                        }
                    ]
                },
                "Authors": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": entry[1]
                            }
                        }
                    ]
                },
                "Venue": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": entry[2]
                            }
                        }
                    ]
                },
                "URL": {
                    "url": entry[3]
                },
                "Hashed Title": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": entry[4]
                            }
                        }
                    ]
                },
            }
        }


class NotionServiceException(Exception):
    pass

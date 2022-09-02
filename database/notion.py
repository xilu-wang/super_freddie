import json
from datetime import datetime, timedelta
from typing import List

import requests

from utils.text_processing import extract_point


class ProcessedTaskLog:
    def __init__(
        self, title: str, point: int, owner: str, raw_log_id: str, executed_at: str
    ):
        self.title = title
        self.point = point
        self.owner = owner
        self.raw_log_id = raw_log_id
        self.executed_at = executed_at


class RawTaskLog:
    def __init__(self, notion_page_id: str, raw_log: str, owner: str, created_at: str):
        self.notion_page_id = notion_page_id
        self.raw_log = raw_log
        self.owner = owner
        self.created_at_str = created_at

    def process_raw_log(self) -> ProcessedTaskLog:
        return ProcessedTaskLog(
            title=self.raw_log,
            point=extract_point(self.raw_log),
            owner=self.owner,
            raw_log_id=self.notion_page_id,
            executed_at=self.created_at_str,
        )


class NotionDatabase:
    def __init__(self, notion_api_token: str, notion_db_id: str):
        self.api_token = notion_api_token
        self.db_id = notion_db_id
        self.db_query_url = f"https://api.notion.com/v1/databases/{self.db_id}/query"
        self.request_headers = {
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def fetch_raw_log_by_days(self, n: int) -> List[RawTaskLog]:
        response = requests.request(
            "POST",
            self.db_query_url,
            headers=self.request_headers,
            data=json.dumps(
                {
                    "filter": {
                        "timestamp": "created_time",
                        "created_time": {
                            "on_or_after": (
                                datetime.now() - timedelta(days=n)
                            ).isoformat()
                        },
                    }
                }
            ),
        )

        log_list = []
        for r in response.json()["results"]:
            prop = r["properties"]
            log_list.append(
                RawTaskLog(
                    notion_page_id=r["id"],
                    raw_log=prop["log"]["title"][0]["plain_text"],
                    owner=prop["owner"]["rich_text"][0]["plain_text"],
                    created_at=r["created_time"],
                )
            )

        return log_list

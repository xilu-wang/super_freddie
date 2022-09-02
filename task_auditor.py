from collections import defaultdict

import click

from database.notion import NotionDatabase


@click.command()
@click.option("--notion_token", type=str)
@click.option("--notion_db_id", type=str)
@click.option("--day", type=int, default=1)
def main(notion_token: str, notion_db_id: str, day: int):
    db = NotionDatabase(notion_token, notion_db_id)
    obj = db.fetch_raw_log_by_days(day)
    count = defaultdict(lambda: 0)
    for o in obj:
        count[o.owner] += o.process_raw_log().point
    for k, v in count.items():
        print(f"{k} has earned {v} points!")


if __name__ == "__main__":
    main()

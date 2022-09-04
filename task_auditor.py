from collections import defaultdict

import click

from database.notion import NotionDatabase


@click.command()
@click.option("--notion_token", type=str)
@click.option("--notion_db_id", type=str)
@click.option("--day", type=int, default=1)
@click.option("--show_details", type=bool, default=False)
def main(notion_token: str, notion_db_id: str, day: int, show_details: bool):
    db = NotionDatabase(notion_token, notion_db_id)
    logs = db.fetch_raw_log_by_days(day)
    count = defaultdict(lambda: 0)
    details = defaultdict(lambda: [])
    for log in logs:
        point = log.process_raw_log().point
        count[log.owner] += point
        details[log.owner].append(
            f"\t{point} point(s) earned by `{log.raw_log}` at {log.created_at_str[5:16].replace('T', ' ')}"
        )

    for k, v in count.items():
        print(f"\n:raised_hands: {k} has earned {v} total points!")

    if show_details:
        for k, v in details.items():
            print(f"\n{k}'s task details:")
            for i in v:
                print(i)


if __name__ == "__main__":
    main()

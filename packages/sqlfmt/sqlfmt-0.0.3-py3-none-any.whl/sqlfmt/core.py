from pathlib import Path

from sqlfluff.api import fix


def format(sql: str) -> str:
    return fix(
        sql,
        config_path=str(Path(__file__).resolve().parent / "sqlfluff.cfg"),
    )

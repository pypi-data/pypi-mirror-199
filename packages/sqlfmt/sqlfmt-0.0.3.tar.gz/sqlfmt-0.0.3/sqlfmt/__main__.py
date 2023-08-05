from pathlib import Path

from typer import Typer

from sqlfmt.core import format

app = Typer()


@app.command()
def main(file_path: str) -> None:
    path = Path(file_path)

    with path.open("r") as f:
        sql = f.read()

    sql = format(sql)

    with path.open("w") as f:
        f.write(sql)


if __name__ == "__main__":
    app()

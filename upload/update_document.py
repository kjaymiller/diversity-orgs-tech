import json

import typer

from connection import app_search, engine_name


def update(filepath: typer.FileText):
    return app_search.put_documents(
        engine_name=engine_name,
        documents=json.load(filepath),
    )


if __name__ == "__main__":
    typer.run(update)

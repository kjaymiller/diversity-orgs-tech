import pandas as pd
import typer

from connection import app_search, engine_name


# TODO: Write Test
def delete_from_index(query):
    """searches the engine for the query and deletes mathches"""
    results = app_search.search(
        engine_name=engine_name,
        body={"query": query},
    )
    ids = [x["id"]["raw"] for x in results["results"]]
    app_search.delete_documents(
        engine_name=engine_name,
        document_ids=ids,
    )


def cleanup(filename: str):
    df = pd.read_json(filename)
    print(f"Original_Count = {df.count()}")
    clean_df = df.drop_duplicates(subset=["name"], keep="last")
    clean_df.to_json(f"{filename}_new.json", orient="records")
    print(f"Original_Count = {clean_df.count()}")


if __name__ == "__main__":
    typer.run(cleanup)

import os
import re
import typing


from connection import  elastic_search
from flask import Flask, flash, redirect, render_template, request
from city_search import city_search
from social_check import social_check



app = Flask(__name__)
app.secret_key = os.urandom(16)
es_index = os.environ.get("ES_INDEX")


def cleanup(form_data):
    """Helper Function to strip out empty field values"""
    return {key:val for key,val in form_data.items() if val} 


def format_form(form_data: dict[str, str]) -> dict[str, typing.Any]:
    """
    Helper function to format the form data for display
    """
    
    doc = city_search(
            es_index=os.environ.get('CITIES_INDEX'),
            document=form_data,
    )
    
    for field in ["technology_focus", "diversity_focus"]:
        doc[field] = re.split(r'\, *', doc[field])
    
    links = re.split(r'\, *', form_data['links'])
    
    for link in links:
        doc.update(social_check(link))
    
    return doc

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("query")
    query = {
        "multi_match": {
            "type": "best_fields",
            "query": q,
         }
    }
    results = elastic_search.search(index=es_index, query=query, size=1000)
    return render_template(
        "search.html",
        results=results,
        query=q,
    )


@app.route("/create/",  methods=["GET", "POST"])
def create_entry():
    if request.method == "POST":
        form_data = dict(request.form)
        doc = format_form(form_data)
        results = elastic_search.index(
            index=es_index,
            document=cleanup(doc),
        )
        flash(f"{doc['name']} created")

        return redirect("/")

    else:
        results = {}
        
        return render_template(
        "create_entry.html",
        results=results,
        form_path="create",
        )


@app.route("/edit/<_id>", methods=["GET", "POST"])
def view_entry(_id):

    if request.method == "POST":
        form_data = dict(request.form)
        doc = format_form(form_data)
        elastic_search.index(
            index=es_index,
            id=_id,
            document=cleanup(doc),
            refresh=True,
        )

        flash(f"{form_data['name']} updated!")
        return redirect(f"/edit/{_id}")

    else:
        results = elastic_search.get(
            index=es_index,
            id=_id,
        )
        return render_template(
            "edit_entry.html",
            results=results,
            form_path="edit",
        )


@app.route("/delete/<_id>")
def delete_documents(_id):
    response = elastic_search.delete(
        index=es_index,
        document=_id,
    )
    flash(f"{_id} Successfully Deleted")
    
    return render_template(
        "index.html",
        results=results,
    )


if __name__ == "__main__":
    app.run(debug=True)
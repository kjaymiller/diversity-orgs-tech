from flask import Flask, render_template, request, redirect, flash
from connection import app_search, engine_name
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/search')
def search():
	q = request.args.get('query')
	body = {
			'query': q,
			'analytics': {
				'tags': ['admin']
			},
			'page': {'size': 50}
	}
	response = app_search.search(engine_name, body=body)
	meta, results = response.values()
	return render_template(
			'search.html',
			meta=meta,
			results=results,
			query=q,
			)

@app.route('/edit/<_id>', methods=['GET', 'POST'])
def view_entry(_id):
	
	if request.method == 'POST':
		form_data = dict(request.form)
		
		for field in ['technology_focus', 'diversity_focus', 'links']:
			form_data[field] = form_data[field].split(',')
		
		app_search.index_documents(
			engine_name=engine_name,
			documents=[form_data],
			params = {
				'analytics': {
				'tags': ['admin']
				},
			}	
		)
		
		flash(f"{form_data['name']} updated!")
		results = form_data

	else:		
		response = app_search.get_documents(
				engine_name=engine_name,
				document_ids = [_id],
				params = {
					'analytics': {
					'tags': ['admin']
					},
				}
		)
		results = response[0] # only returning one entry
	return render_template(
		'edit_entry.html',
		results=results,
	)

@app.route('/delete/<_id>')
def delete_documents(_id):		
	response = app_search.delete_documents(
			engine_name=engine_name,
			document_ids = [_id],
			params = {
				'analytics': {
				'tags': ['admin']
				},
			}
	)
	flash(f'{_id} Successfully Deleted')
	results = response[0] # only returning one entry
	
	return render_template(
	'index.html',
	results=results,
)
	
if __name__ == '__main__':
	app.run(debug=True)
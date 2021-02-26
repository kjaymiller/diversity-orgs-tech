// Customize this 'myform.js' script and add it to your JS bundle.
// Then import it with 'import MyForm from "./myform.js"'.
// Finally, add a <MyForm/> element whereever you wish to display the form.

import React from "react";
import {Link} from 'react-router-dom';

export default class AddOrg extends React.Component {
  constructor(props) {
    super(props);
    this.submitForm = this.submitForm.bind(this);
    this.state = {
      status: ""
    };
  }

  render() {
    const { status } = this.state;
    return (
    <div className="container mx-auto my-3">
        <h1 className="text-4xl font-semibold py-2">Did we miss one?</h1>
        <p> Help us out and add the information for the organization. We'll take a look at get it added as soon as possible.</p>
        <h2 className="my-3">Unsure if your organization belongs? Check the <Link className="underline font-bold" to="mission-statement">Mission Statement</Link></h2>
        <hr />
      <form
        onSubmit={this.submitForm}
        action="https://formspree.io/f/mnqolonp"
        method="POST"
        className="mt-5 lg:w-1/2"
      >
        <div className="my-2">
        <label className="mx-2 font-bold">Email:</label>
        <input className="lg:w-1/2 text-sm border p-1 rounded-lg" placeholder="me@example.com" type="email" name="org-name" />
            <div>
                <small className="italic mx-3 my-2 p-2">This email is only used to notify you if we have questions and is entirely optional</small>
            </div>
        </div>
        <div className="my-2">
        <label className="mx-2 font-bold">Organization Name:</label>
        <input className="lg:w-1/2 text-sm border p-1 rounded-lg" type="text" name="org-name" placeholder="New or Existing Diversity Org" />
        </div>
        <div className="my-2">
        <label className="mx-2 font-bold">Organization Website:</label>
        <input className="lg:w-1/2 text-sm border p-1 rounded-lg" type="url" name="url" placeholder="https://neworg.example.com" />
        </div>
        <div>
            <div>
                <label  className="mx-2 font-bold">Comments:</label>
            </div>
            <div>
                <textarea cols="80" className="mx-4 text-sm border p-2 rounded-lg" placeholder="Any information that you can to help us make the correct change" name="url" />
            </div>
        </div>
        <div className="my-2">
        {status === "SUCCESS" ? <p>Thanks! We'll review this! </p> : <button className="border px-4 py-1 mt-4 rounded-lg shadow hover:from-purple-200 from-pink-200 bg-gradient-to-br to-purple-400 hover:shadow-xl">Submit</button>}
        {status === "ERROR" && <p>Ooops! There was an error.</p>}
        </div>
      </form>
    </div>
    );
  }

  submitForm(ev) {
    ev.preventDefault();
    const form = ev.target;
    const data = new FormData(form);
    const xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.onreadystatechange = () => {
      if (xhr.readyState !== XMLHttpRequest.DONE) return;
      if (xhr.status === 200) {
        form.reset();
        this.setState({ status: "SUCCESS" });
      } else {
        this.setState({ status: "ERROR" });
      }
    };
    xhr.send(data);
  }
}

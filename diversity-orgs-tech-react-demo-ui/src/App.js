import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from 'react-router-dom';

import AddOrg from './Add.js';
import Home from './Home.js';
import Ethics from './ethics';


export default function App() {
    return (
        <div>
        <Router>
        <div class="py-3 border">
            <div className="container my-3 mx-auto">
                <div className="xl:flex items-center"> 
                    <h1><Link to="/">DiversityOrgs.Tech</Link>
                <span className="my-4 text-3xl font-thin"> - Find the tech community that's right for you.</span></h1>
                </div>
          </div>
        </div>
            <Switch>
                <Route path="/addorg"><AddOrg /></Route>
                <Route path="/ethics"><Ethics /></Route>
                <Route path="/"><Home /></Route>
            </Switch>
        </Router>
        </div>
    );
}

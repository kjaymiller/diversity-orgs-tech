import React from 'react';
import { Link } from 'react-router-dom';
import Search from './search.js';

export default function Home() {
    return (
        <div className="text-gray-700">
            <div className="my-4 p-2 container mx-auto">
                <div className="flex justify-between items-center p-3 my-8 rounded-lg bg-gradient-to-r from-gray-100 to-indigo-200">
                    <div className="w-1/2 pl-8">
                        <h1 className="text-5xl my-3 font-extralight text-gray-600 font-bold">You <span class="font-bold text-indigo-500 uppercase">belong</span></h1>
                        <div className="text-2xl p-2">
                            <p className="my-2">Search for groups based on their Representation goals or their tech stack.</p>
                            <p className="my-2">If you know of an organization that we're missing, <Link to="/addorg" className="underline">let us know</Link>.</p>
                        </div>
                    </div>
                    <div className="hidden lg:block rounded-xl w-1/4">
                        <img alt="person-sitting-on-bench" className="rounded-2xl" src="./pexels-ono-kosuki-5647210.jpg" />
                    </div>
                </div>
                <div className="my-3">
                    <h2 className="my-4 text-2xl font-thin"> Things you can search for:</h2>
                    <div className="my-3 pl-4 text-xl font-bold">
                        <h2 className="">City, State, Region</h2>
                        <h2 className="">Under-Represented Group (See <Link className="underline" to="/ethics">the list</Link> of who is covered)</h2>
                        <h2 className="">Technology or Stack</h2>
                   </div>
               </div>
                <Search />
            </div>
        </div>
    );
}

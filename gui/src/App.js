import React, { useState, useEffect } from 'react';
import { Switch, Route } from 'react-router-dom';
import './style.css';

import { Home } from './Home.js';
import { Recipes } from './Recipes.js';
import { RecipeDetails } from './RecipeDetails.js';
import { ReactionHistory } from './ReactionHistory'
import { Tests } from './Tests.js';
import { Settings } from './Settings.js';
import { Status } from './Status.js';

import { apiUrl } from './utils.js';

export function App() {
	const [status, setStatus] = useState();
	const getStatus = () => {
		fetch(apiUrl + 'status')
			.then(response => response.json())
			.then(data => setStatus(data));
	};
	useEffect(() => {
		const interval = setInterval(() => {
			getStatus();
		}, 1000);
		return () => clearInterval(interval);
	}, []);
	console.log("status: ", status);
	//these are the routes. is it in a div instead of Router for any reason?
	//^i think becuase in style.css it sets the maybe-size of the screen
	return (
		<div className='lcd-wrapper'>
			<Switch>
				<Route exact path='/'>
					<Home status={status} />
				</Route>

				<Route exact path='/recipes'>
					<Recipes />
				</Route>

				<Route path='/recipes/:recipeName'>
					<RecipeDetails />
				</Route>

				<Route path='/reaction-history'>
					<ReactionHistory />
				</Route>

				<Route path='/tests'>
					<Tests />
				</Route>

				<Route path='/settings'>
					<Settings />
				</Route>

				<Route path='/status'>
					<Status status={status}/>
				</Route>
			</Switch>
		</div>
	);
}

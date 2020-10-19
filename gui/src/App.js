import React, { useState, useEffect } from 'react';
// import { Switch, Route, Link } from 'react-router-dom';
import { Switch, Route } from 'react-router-dom';
// import { Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
// import { Header } from './Header.js';
import { Home } from './Home.js';
import { Recipes } from './Recipes.js';
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

	console.log(status);

	return (
		<div className='lcd-wrapper'>
			<Switch>
				<Route exact path='/'>
					<Home status={status} />
				</Route>

				<Route path='/recipes'>
					<Recipes />
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

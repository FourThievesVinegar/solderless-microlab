import React, { useState, useEffect } from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { Home } from './Home.js';
import { Reactions } from './Reactions.js';
import { Tests } from './Tests.js';
import { Settings } from './Settings.js';
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
					<Home />
				</Route>

				<Route path='/reactions'>
					<Reactions />
				</Route>

				<Route path='/tests'>
					<Tests />
				</Route>

				<Route path='/settings'>
					<Settings />
				</Route>
			</Switch>
		</div>
	);
}

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
	//this creates a variable 'status', initializes its value to null, 
	//and says that to change the state value of 'status' we use setStatus
	const [status, setStatus] = useState();
	//this just sends a get request(?) to 'http://localhost(or whatever the user has):5000/status'
	const getStatus = () => {
		fetch(apiUrl + 'status')
			//once it gets a response from the server, it turns it into object 
			.then(response => response.json())
			//and updates the state value of 'status' to be the value of the data it gets back
			.then(data => setStatus(data));
	};
	//this requests the status every 1000 milliseconds (1 second)
	useEffect(() => {
		const interval = setInterval(() => {
			getStatus();
		}, 1000);
		return () => clearInterval(interval);
	}, []);
	//i'm a little confused why this happens every time status is updated
	console.log(status);
	//these are the routes. is it in a div instead of Router for any reason?
	//^i think becuase in style.css it sets the maybe-size of the screen
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

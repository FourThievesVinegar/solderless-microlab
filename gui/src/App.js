import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { Home } from './Home.js';
import { Reactions } from './Reactions.js';
import { Settings } from './Settings.js';

export function App() {
	return (
		<div className='lcd-wrapper'>
			<Switch>
				<Route exact path='/'>
					<Home />
				</Route>

				<Route path='/reactions'>
					<Reactions />
				</Route>

				<Route path='/settings'>
					<Settings />
				</Route>
			</Switch>
		</div>
	);
}

import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function App() {
	return (
		<div className='lcd-wrapper'>
			<Header>Home</Header>
		</div>
	);
}

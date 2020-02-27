import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Tests() {
	return (
		<div>
			<Header>Hardware Tests</Header>

			<div className='button-menu'>
				<Button onClick={console.log}>
					Test Relays
				</Button>
			</div>
		</div>
	);
}

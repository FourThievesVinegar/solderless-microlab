import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Home() {
	return (
		<div>
			<Header>Home</Header>

			<div className='button-menu'>
				<Button as={Link} to='/reactions'>
					Reactions
				</Button>

				<Button as={Link} to='/settings'>
					Settings
				</Button>
			</div>
		</div>
	);
}

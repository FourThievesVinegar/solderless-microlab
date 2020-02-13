import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';

export function App() {
	return (
		<div className='lcd-wrapper'>
			<Menu>
				<Menu.Item
					icon
					onClick={console.log}
				>
					<Icon name='chevron left' />
				</Menu.Item>

				<Menu.Item header>
					Home
				</Menu.Item>

				<Menu.Item
					icon
					position='right'
					as={Link}
					to='/'
				>
					<Icon name='home' />
				</Menu.Item>
			</Menu>
		</div>
	);
}

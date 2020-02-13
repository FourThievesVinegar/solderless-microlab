import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Icon, Menu, Segment } from 'semantic-ui-react';

export function Header(props) {
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
					{props.children}
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

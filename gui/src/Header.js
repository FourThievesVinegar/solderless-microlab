import React from 'react';
// import { Switch, Route, Link, useHistory, useRouteMatch } from 'react-router-dom';
import { Link, useHistory, useRouteMatch } from 'react-router-dom';
// import { Icon, Menu, Segment } from 'semantic-ui-react';
import { Icon, Menu } from 'semantic-ui-react';

export function Header(props) {
	const history = useHistory();
	const match = useRouteMatch();

	return (
		<div>
			<Menu>
				<Menu.Item
					icon
					onClick={history.goBack}
					disabled={match.path === '/'}
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
					to='/settings'
				>
					<Icon name='setting' />
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

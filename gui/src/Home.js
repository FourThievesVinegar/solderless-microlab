import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Home(props) {
	const { status } = props;

	return (
		<div>
			<Header>Home</Header>

			<div className='button-menu'>
				{status &&
					<Button as={Link} to='/status'>
						{status.recipe.toUpperCase()} Status
					</Button>
				}

				<Button as={Link} to='/recipes'>
					Recipes
				</Button>

				<Button as={Link} to='/tests'>
					Hardware Tests
				</Button>

				<Button as={Link} to='/settings'>
					Settings
				</Button>
			</div>
		</div>
	);
}

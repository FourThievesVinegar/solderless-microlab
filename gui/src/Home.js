import React from 'react';
// import { Switch, Route, Link } from 'react-router-dom';
import { Link } from 'react-router-dom';
// import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import { Button } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Home(props) {
	//this is the same as saying status = props.status
	const { status } = props;

	return (
		<div>
			<Header>Home</Header>

			<div className='button-menu'>
				{(status && status.recipe) ?
					//if there's a recipe in progress, give a link to see its status
					//if not, offer option to start reaction
					//doing this ternary operator leads to it showing the
					//second option for up to a second before the server
					//comes back with the status.
					//is this a case for useEffect?
					<div>
						<p>{status.recipe} reaction in progress.</p>
						<Button as={Link} to='/status'>
							Resume {status.recipe.toUpperCase()} Reaction
							{/* maybe this would be a good place to preview next step? */}
						</Button>
					</div>
					:
					<Button as={Link} to='/recipes'>Start a Reaction</Button>
				}
				
				<Button as={Link} to='/reaction-history'>
					Reaction History
				</Button>

				{/* should this be a verb like 'view recipes' (as opposed to choose one) */}
				<Button as={Link} to='/recipes'>
					Recipes
				</Button>

				{/* should hardware be test-able mid recipe? maybe there
				should be one home screen for if there is a recipe going,
				and one for if there isn't? */}
				<Button as={Link} to='/tests'>
					Test Hardware
				</Button>
			</div>
		</div>
	);
}

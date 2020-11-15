import React, { useState, useEffect } from 'react';
// import { Switch, Route, Link, useHistory } from 'react-router-dom';
import { useHistory } from 'react-router-dom';
// import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import { Button} from 'semantic-ui-react';

import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function Recipes() {
	const [recipies, setRecipies] = useState(false);
	const history = useHistory();

	useEffect(() => {
		fetch(apiUrl + 'list')
			.then(response => response.json())
			.then(data => setRecipies(data));
	}, []);

	// const startRecipe = (name) => {
	// 	fetch(apiUrl + 'start/' + name)
	// 		.then(response => response.json())
	// 		.then(data => history.push('/status'));
	// };

	console.log(recipies);

	return (
		<div>
			<Header>Recipes</Header>

			{recipies ?
				<div className='button-menu'>
					{recipies.map(recipe =>
						// click on recipe to view details
						<Button key={recipe} onClick={() => history.push(`/recipes/${recipe}`)}>
							{recipe.toUpperCase()} (click to view details)
						</Button>
					)}
				</div>
			:
				<p>Loading...</p>
			}
		</div>
	);
}

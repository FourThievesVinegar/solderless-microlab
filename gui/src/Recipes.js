import React, { useState, useEffect } from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function Recipes() {
	const [recipies, setRecipies] = useState(false);

	useEffect(() => {
		fetch(apiUrl + 'list')
			.then(response => response.json())
			.then(data => setRecipies(data));
	}, []);

	console.log(recipies);

	return (
		<div>
			<Header>Recipes</Header>

			{recipies ?
				<div className='button-menu'>
					{recipies.map(x =>
						<Button>
							{x.toUpperCase()}
						</Button>
					)}
				</div>
			:
				<p>Loading...</p>
			}
		</div>
	);
}

import React, { useState } from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function TestButton(props) {
	const { name, label } = props;
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(false);

	const runTest = (e) => {
		if (loading) return;
		setLoading(true);

		fetch(apiUrl + 'test/' + name)
		.then(res => {
			setLoading(false);
			setError(false);
		})
		.catch(err => {
			setLoading(false);
			setError(true);
		});
	};

	return (
		<Button onClick={runTest} loading={loading}>
			{error ? 'Error' : label}
		</Button>
	);
};

export function Tests() {
	return (
		<div>
			<Header>Hardware Tests</Header>

			<div className='button-menu'>
				<Button as={Link} to='/relays'>
					Relays
					</Button> 

				 <Button as={Link} to='/therm'>
					USB Thermometer
					</Button>

				<Button as={Link} to='/motors'>
					Stirring Motors
				</Button>

				<Button as={Link} to='/stirring'>
					Stirring Rod
				</Button>
			</div>
		</div>
	);
};

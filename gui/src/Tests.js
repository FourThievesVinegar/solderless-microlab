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
				<TestButton name='relays' label='Test Relays' />
			</div>
			<div className='button-menu'>
				<TestButton name='usbtherm' label='USB Thermometer' />
			</div>
			<div className='button-menu'>
				<TestButton name='motors' label='Stepper Motors' />
			</div>
			<div className='button-menu'>
				<TestButton name='stirringrod' label='Stirring Rod' />
			</div>
		</div>
	);
};

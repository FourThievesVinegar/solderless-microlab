import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Status(props) {
	const { status } = props;

	return (
		<div>
			<Header>Status</Header>

			{status ?
				<p>{JSON.stringify(status)}</p>
			:
				<p>Loading...</p>
			}
		</div>
	);
}

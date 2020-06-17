import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';

export function Recipes() {
	return (
		<div>
			<Header>Recipes</Header>

			<p>Recipes page here...</p>
		</div>
	);
}

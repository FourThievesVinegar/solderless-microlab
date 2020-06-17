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
				<div className='button-menu'>
					<p>{status.message}</p>

					{status.options.map(x =>
						<Button>
							{x}
						</Button>
					)}
				</div>
			:
				<p>Loading...</p>
			}
		</div>
	);
}

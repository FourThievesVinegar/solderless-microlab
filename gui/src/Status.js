import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function Status(props) {
	const { status } = props;

	const selectOption = (option) => {
		fetch(apiUrl + 'select/option/' + option)
			.then(response => response.json())
			.then(data => console.log(data));
	};

	return (
		<div>
			<Header>Status</Header>

			{status ?
				<div className='button-menu'>
					<p>{status.message}</p>

					{status.options.map(x =>
						<Button key={x} onClick={() => selectOption(x)}>
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

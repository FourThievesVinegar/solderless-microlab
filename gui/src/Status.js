import React, { useState, useEffect } from 'react';
// import { Switch, Route, Link } from 'react-router-dom';
// import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import { Button } from 'semantic-ui-react';
import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function Status(props) {
	const { status } = props;
	const [loading, setLoading] = useState(false);

	const selectOption = (option) => {
		if (loading) return;
		setLoading(true);

		fetch(apiUrl + 'select/option/' + option)
			.then(response => response.json())
			.then(data => console.log(data));
	};

	useEffect(() => {
		setLoading(false);
	}, [status && status.step]);

	return (
		<div>
			<Header>Status</Header>

			{status ?
				<div className='button-menu'>
					<p>{status.message}</p>

					{status.options.map(x =>
						<Button key={x} onClick={() => selectOption(x)} loading={loading}>
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

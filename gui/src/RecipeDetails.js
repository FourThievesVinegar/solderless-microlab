import React, { useState, useEffect } from 'react';
// import { Switch, Route, Link, useHistory } from 'react-router-dom';
import { useParams} from 'react-router-dom';
import { useHistory } from 'react-router-dom';
// import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import { Button } from 'semantic-ui-react';

import './style.css';
import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function RecipeDetails() {
    const [recipies, setRecipies] = useState(false);
    const history = useHistory();
    const { recipeName } = useParams();

    // get specific recipe details based on param(recipe name)? or would it be passed thru?
    // useEffect(() => {
    //     fetch(apiUrl + 'list')
    //         .then(response => response.json())
    //         .then(data => setRecipies(data));
    // }, []);

    const startRecipe = (name) => {
    	fetch(apiUrl + 'start/' + name)
    		.then(response => response.json())
    		.then(data => history.push('/status'));
    };

    console.log(recipies);

    return (
        <div>
            <Header>Recipe Details</Header>
            <h1>{ recipeName }</h1>
            <p>more details would go here</p>
            <p>would they come from props? redux store?</p>
            <Button onClick={() => startRecipe(recipeName)}>
                Start A Reaction Using This Recipe
            </Button>
            <p>this button should only be clickable if there isn't a reaction going</p>
        </div>
    );
}

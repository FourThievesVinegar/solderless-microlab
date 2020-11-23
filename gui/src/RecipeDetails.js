import React, { useState, useEffect } from 'react';
import { useParams} from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import { Button } from 'semantic-ui-react';

import { Header } from './Header.js';
import { apiUrl } from './utils.js';

export function RecipeDetails() {
    const [recipeDetails, setRecipeDetails] = useState(false);
    const history = useHistory();
    const { recipeName } = useParams();

    // fetch recipe details, such as steps, ingredients, time
    useEffect(() => {
        fetch(apiUrl + '___________')
            .then(response => response.json())
            .then(data => setRecipeDetails(data));
    }, []);

    const startRecipe = (name) => {
    	fetch(apiUrl + 'start/' + name)
    		.then(response => response.json())
    		.then(data => history.push('/status'));
    };

    console.log("recipe details:", recipeDetails);

    return (
        <div>
            <Header>Recipe Details</Header>
            <h1>{ recipeName }</h1>
                {/* 
                display details of the selected recipe.
                having the fetch be based on the url makes it so that if a user visits 
                the address it'll get the right info- but is that even relevant with the hardware being used?
                If no one's ever going to visit .../recipes/this-specific-recipe other than by clicking on 
                the name in Recipes.js, then the fetch could just come from the "see details" button 
                in Recipes and be provided to this component with props or with a redux store.
                */}

                {recipeDetails ?
                    // might make sense to have individual "Materials", "Time", "Steps" components 
                    // if they might be reused outside of this RecipeDetails component (like on a confirmation "are you ready to start this for real?" screen?)
                    <>
                    <h2>Materials Needed:</h2>
                        <ul>
                            {/* map out materials */}
                        </ul>
                    <h2>Time Needed:</h2>
                        {/* total time? which steps are time sensitive and how long between them? */}
                    <h2>Steps:</h2>
                        <ul>
                            {/* map out steps */}
                            {/* maybe "Step.js" component if it'll look the same as when a reaction's in progress */}
                        </ul>
                    </>
                    :
                    <p>loading...</p>
                }

            {/* this button should only be clickable/present if there isn't a reaction going, 
            meaning this component needs to know status, either from props passed to it 
            or from a redux store store.*/}
            <Button onClick={() => startRecipe(recipeName)}>
                Start A Reaction Using This Recipe
            </Button>
        </div>
    );
}

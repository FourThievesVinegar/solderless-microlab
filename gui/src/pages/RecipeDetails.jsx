import humanizeDuration from 'humanize-duration';
import { capitalize, get, isArray, isEmpty, isNumber, reduce, toNumber } from 'lodash';
import React, { useEffect, useState } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { Button } from 'semantic-ui-react';
import "../styles/app.css";
import { apiUrl } from '../utils';

export function RecipeDetails() {
    const [recipeDetails, setRecipeDetails] = useState({});
    const history = useHistory();
    const { recipeName } = useParams();

    // fetch recipe details, such as steps, ingredients, time
    useEffect(() => {
        fetch(apiUrl + 'recipe/' + recipeName)
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
        <section className='page recipe-details'>
            <h1>{capitalize(recipeName)}</h1>
            {/* 
                display details of the selected recipe.
                having the fetch be based on the url makes it so that if a user visits 
                the address it'll get the right info- but is that even relevant with the hardware being used?
                If no one's ever going to visit .../recipes/this-specific-recipe other than by clicking on 
                the name in Recipes.js, then the fetch could just come from the "see details" button 
                in Recipes and be provided to this component with props or with a redux store.
                */}

            {!isEmpty(recipeDetails) ?
                // might make sense to have individual "Materials", "Time", "Steps" components 
                // if they might be reused outside of this RecipeDetails component (like on a confirmation "are you ready to start this for real?" screen?)
                <>
                    <MaterialsNeeded materials={recipeDetails.materials} />
                    <TimeNeeded steps={recipeDetails.steps} />
                    <Steps steps={recipeDetails.steps} />
                </>
                :
                <p>loading...</p>
            }

            {/* this button should only be clickable/present if there isn't a reaction going, 
            meaning this component needs to know status, either from props passed to it 
            or from a redux store store.*/}
            <Button 
                color="green" 
                onClick={() => {
                    startRecipe(recipeName)
                    history.push('/status')
                }}
            >
                Start A Reaction Using This Recipe
            </Button>
        </section>
    );
}

function MaterialsNeeded({ materials }) {
    let body;
    if (isArray(materials) && materials.length > 0) {
        body = <ol>
            {materials.map((material) => <li>
                {material.description}
            </ li>)}
        </ol>;
    } else {
        body = <span>No materials needed</span>;
    }

    return <>
        <h3>Materials Needed:</h3>
        {body}
    </>
}

/**
 * total time? which steps are time sensitive and how long between them?
 * */
function TimeNeeded({ steps }) {
    const [timePerStep, setTimePerStep] = useState(10);

    if (!isArray(steps) || steps.length < 1) {
        return <></>
    }

    const waitTime = reduce(steps, (sum, step) => {
        return sum + get(step, 'parameters.time', 0)
    }, 0);

    function TimeNeededSection({ label, seconds }) {
        return <p>
            <b>{`${label}: `}</b>
            <span>{humanizeDuration(seconds * 1000)}</span>
        </p>
    }

    return <>
        <h3>Time Needed:</h3>

        <p>
            <span>
                How many seconds, on average, will you take to do each manual task?{' '}
                <input
                    name='averageDuration'
                    type='number'
                    value={timePerStep}
                    onChange={(e) => {
                        const newValue = toNumber(e.target.value);
                        if (isNumber(newValue) && newValue > 0) {
                            setTimePerStep(newValue)
                        }
                    }}
                />
            </span>
        </p>

        <TimeNeededSection label='Time needed for manual tasks' seconds={timePerStep * steps.length} />
        <TimeNeededSection label='Time needed for manual tasks' seconds={waitTime} />
        <TimeNeededSection label='Total time needed' seconds={timePerStep * steps.length + waitTime} />
    </>
}

function Steps({ steps }) {
    if (!isArray(steps) || steps.length < 1) {
        return <span>No steps</span>
    }

    return <>
        <h3>Steps:</h3>
        <ol>
            {steps.map((step) => <li>
                {step.message}
            </ li>)}
        </ol>
    </>
}

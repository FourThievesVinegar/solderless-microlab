import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { listRecipes } from '../utils'

// This component, Recipes.js, requests a list of recipe names to display on the screen
// It seems like App.js could also request this list and make it available to Recipes.js with redux.

// It makes sense to use this component whenever the user wants to see a list of all the recipes (obviously)
// which would either be before choosing a reaction to run, or just browsing
// If they select a recipe when they're in browsing mode, they probably want to see a list of materials and steps.
// If they select a recipe when they're in 'I want to run a reaction' mode, they probably want a quick summary/confirmation before proceeding
// These two modes could be differentiated based on parent component passing props to this component
// or in the redux store with a reducer

export function Recipes() {
  const [recipies, setRecipies] = useState(false)
  const history = useHistory()

  useEffect(() => {
    listRecipes(setRecipies)
  }, [])

  console.log('recipes:', recipies)

  return (
    <section className="page recipes-page">
      <h1>Recipe list</h1>
      {recipies ? (
        <div className="button-list">
          {recipies.map(recipe => (
            // click on recipe to view details
            <Button key={recipe} onClick={() => history.push(`/recipes/${recipe}`)}>
              {recipe.toUpperCase()} (click to view details)
            </Button>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </section>
  )
}

import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { listRecipes } from '../utils'
import { RecipeUpload } from '../components/RecipeUpload'

export function Recipes() {
  const [recipies, setRecipies] = useState(false)
  const history = useHistory()

  useEffect(() => {
    listRecipes(setRecipies)
  }, [])

  return (
    <section className="page recipes-page">
      <h1>Recipe list</h1>
      {recipies ? (
        <div className="button-list">
          {recipies.map(recipe => (
            // click on recipe to view details
            <Button key={recipe} color="blue" onClick={() => history.push(`/recipes/${recipe}`)}>
              {recipe.toUpperCase()}
            </Button>
          ))}
          <h2>Upload a Recipe</h2>
          <RecipeUpload />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </section>
  )
}

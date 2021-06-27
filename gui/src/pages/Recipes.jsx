import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { listRecipes } from '../utils'

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
            <Button key={recipe} onClick={() => history.push(`/recipes/${recipe}`)}>
              {recipe.toUpperCase()}
            </Button>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </section>
  )
}

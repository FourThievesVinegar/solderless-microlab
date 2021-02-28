import React, { useState } from 'react'
import { useParams, useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { startRecipe } from '../utils'

export function RecipeDetails() {
  const [recipeDetails, setRecipeDetails] = useState(false)
  const { recipeName } = useParams()
  const history = useHistory()

  const handleStartClick = () => {
    startRecipe(recipeName)
    history.push('/status')
  }

  return (
    <section className="page recipe-details">
      <h1>{recipeName}</h1>

      {recipeDetails ? (
        // might make sense to have individual "Materials", "Time", "Steps" components
        // if they might be reused outside of this RecipeDetails component (like on a confirmation "are you ready to start this for real?" screen?)
        <>
          <h2>Materials Needed:</h2>
          <ul>{/* map out materials */}</ul>
          <h2>Time Needed:</h2>
          {/* total time? which steps are time sensitive and how long between them? */}
          <h2>Steps:</h2>
          <ul>
            {/* map out steps */}
            {/* maybe "Step.js" component if it'll look the same as when a reaction's in progress */}
          </ul>
        </>
      ) : (
        <p>loading...</p>
      )}

      <Button color="green" onClick={() => handleStartClick()}>
        Start A Reaction Using This Recipe
      </Button>
    </section>
  )
}

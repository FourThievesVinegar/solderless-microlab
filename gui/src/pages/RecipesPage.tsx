import React, { useState, useEffect, useContext } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { RecipeUpload } from '../components/RecipeUpload'
import SettingsContext from '../contexts/Settings'
import { SOUNDS, useAudio } from '../hooks/useAudio'
import { listRecipes } from '../utils'

export function RecipesPage() {
  const [recipes, setRecipes] = useState<false | string[]>(false)
  const history = useHistory()
  const { settings } = useContext(SettingsContext)

  const [introPlaying, playIntroSound] = useAudio(SOUNDS.INTRO)

  const reloadRecipes = () => {
    listRecipes(setRecipes)
  }

  useEffect(() => {
    reloadRecipes()
    if (!settings.muteIntroSound) {
      playIntroSound(true)
    }
  }, [])

  return (
    <section className="page recipes-page">
      <h1>Recipe list</h1>
      {recipes ? (
        <div className="button-list">
          {recipes.map((recipe, i) => (
            // click on recipe to view details
            <Button key={i} color="blue" onClick={() => history.push(`/recipes/${recipe}`)}>
              {recipe.toUpperCase()}
            </Button>
          ))}
          <h2>Upload a Recipe</h2>
          <RecipeUpload onUpload={reloadRecipes} />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </section>
  )
}

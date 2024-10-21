import React, { useState, useEffect, useContext } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { RecipeUpload } from '../components/RecipeUpload'
import SettingsContext from '../contexts/Settings'
import { SOUNDS, useAudio } from '../hooks/useAudio'
import { listRecipes, capitalize } from '../utils'
import { useTranslation } from 'react-i18next'

export function RecipesPage() {
  const { t } = useTranslation()
  const [recipes, setRecipes] = useState<false | string[]>(false)
  const history = useHistory()
  const { settings } = useContext(SettingsContext)

  const [introPlaying, playIntroSound] = useAudio(SOUNDS.INTRO)

  const sortAndSaveRecipes = (recipes: string[]) => {
    recipes.sort((a, b) => {
      if (capitalize(a) > capitalize(b)) {
        return 1
      } else {
        return -1
      }
    })
    setRecipes(recipes)
  }

  const reloadRecipes = () => {
    listRecipes(sortAndSaveRecipes)
  }

  useEffect(() => {
    reloadRecipes()
    if (!settings.muteIntroSound) {
      playIntroSound(true)
    }
  }, [])

  return (
    <section className="page recipes-page">
      <h1>{t('recipe-list')}</h1>
      {recipes ? (
        <div className="button-list">
          {recipes.map((recipe, i) => (
            // click on recipe to view details
            <Button key={i} color="blue" onClick={() => history.push(`/recipes/${recipe}`)}>
              {recipe.toUpperCase()}
            </Button>
          ))}
          <h2>{t('upload-recipe-button-label')}</h2>
          <RecipeUpload onUpload={reloadRecipes} />
        </div>
      ) : (
        <p>{t('loading-placeholder')}</p>
      )}
    </section>
  )
}

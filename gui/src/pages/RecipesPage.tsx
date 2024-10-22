import React, { useState, useRef, useEffect, useContext } from 'react'
import { useHistory } from 'react-router-dom'
import { Button } from 'semantic-ui-react'

import { RecipeUpload } from '../components/RecipeUpload'
import SettingsContext from '../contexts/Settings'
import { SOUNDS, useAudio } from '../hooks/useAudio'
import { listRecipes, capitalize } from '../utils'
import { useTranslation } from 'react-i18next'

import './RecipesPage.scss'
import { getDefaultFormatCodeSettings } from 'typescript'

export function RecipesPage() {
  const { t } = useTranslation()
  const [recipes, setRecipes] = useState<[] | string[]>([])
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

  const recipeAnchorMap: { [key: string]: true | undefined } = {}

  recipes.forEach(recipe => {
    const startingLetter: string = recipe[0].toUpperCase()
    if (!recipeAnchorMap[startingLetter]) {
      recipeAnchorMap[startingLetter] = true
    }
  })

  return (
    <section className="page recipes-page">
      <section className="recipes-left-nav">
        {Object.keys(recipeAnchorMap).map(key => {
          return (
            <Button
              key={key}
              color="purple"
              onClick={() => {
                document.querySelector('.recipe-anchor-' + key)?.scrollIntoView()
              }}>
              {key}
            </Button>
          )
        })}
      </section>
      <section className="recipes-list">
        <h1>{t('recipe-list')}</h1>
        {recipes.length ? (
          <div className="button-list">
            {recipes.map((recipe, i) => {
              const firstLetter = recipe[0].toUpperCase()
              const recipeAnchor = recipeAnchorMap[firstLetter] ? (
                <a className={`recipe-anchor-${firstLetter}`}></a>
              ) : null
              recipeAnchorMap[firstLetter] = undefined

              return (
                <>
                  {recipeAnchor}
                  <Button key={i} color="blue" onClick={() => history.push(`/recipes/${recipe}`)}>
                    {recipe.toUpperCase()}
                  </Button>
                </>
              )
            })}
            <h2>{t('upload-recipe-button-label')}</h2>
            <RecipeUpload onUpload={reloadRecipes} />
          </div>
        ) : (
          <p>{t('loading-placeholder')}</p>
        )}
      </section>
    </section>
  )
}

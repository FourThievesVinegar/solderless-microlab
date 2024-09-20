import humanizeDuration from 'humanize-duration'
import { capitalize, get, isArray, isEmpty, reduce } from 'lodash'
import React, { useEffect, useState } from 'react'
import { useHistory, useParams } from 'react-router-dom'
import { Button } from 'semantic-ui-react'
import { getRecipe, startRecipe } from '../utils'
import { MicrolabRecipe, RecipeMaterial, RecipeStep } from '../microlabTypes'
import { useTranslation } from 'react-i18next'

import './RecipeDetailsPage.scss'

export function RecipeDetails() {
  const { t } = useTranslation()
  const [recipeDetails, setRecipeDetails] = useState<MicrolabRecipe>()
  const history = useHistory()
  const { recipeName } = useParams<any>()

  // fetch recipe details, such as steps, ingredients, time
  useEffect(() => {
    getRecipe(recipeName).then(setRecipeDetails)
  }, [recipeName])

  const StartRecipeButton = () => {
    return (
      <Button
        color="purple"
        onClick={() => {
          startRecipe(recipeName).then(data => history.push('/status'))
        }}>
        {t('start-reaction-button-text')}
      </Button>
    )
  }

  return (
    <section className="page recipe-details">
      <h1>{capitalize(recipeName)}</h1>
      <StartRecipeButton />

      {recipeDetails && !isEmpty(recipeDetails) ? (
        <>
          <MaterialsNeeded materials={recipeDetails.materials} />
          <TimeNeeded steps={recipeDetails.steps} />
          <Steps steps={recipeDetails.steps} />
        </>
      ) : (
        <p>{t('loading-placeholder')}</p>
      )}
      <StartRecipeButton />
    </section>
  )
}

function MaterialsNeeded({ materials }: { materials: RecipeMaterial[] }) {
  const { t } = useTranslation()
  let body
  if (isArray(materials) && materials.length > 0) {
    body = (
      <ol>
        {materials.map((material, index) => (
          <li key={`material-${index}`}>{material.description}</li>
        ))}
      </ol>
    )
  } else {
    body = <span>{t('no-materials-needed')}</span>
  }

  return (
    <>
      <h3>{t('recipe-materials-needed')}</h3>
      {body}
    </>
  )
}

/**
 * total time? which steps are time sensitive and how long between them?
 * */
function TimeNeeded({ steps }: { steps: RecipeStep[] }) {
  const { t } = useTranslation()
  if (!isArray(steps) || steps.length < 1) {
    return <></>
  }

  const waitTime = reduce(
    steps,
    (sum: number, step: { tasks: any }) => {
      return sum + reduce(step.tasks, (max: number, task: any) => Math.max(get(task, 'parameters.time', 0), max), 0)
    },
    0,
  )

  function TimeNeededSection({ label, seconds }: { label: string; seconds: number }) {
    return (
      <p>
        <b>{`${label}: `}</b>
        <span>{humanizeDuration(seconds * 1000)}</span>
      </p>
    )
  }

  return (
    <>
      <h3>{t('recipe-time-needed')}</h3>
      <TimeNeededSection label={t('recipe-time-needed-for-tasks')} seconds={waitTime} />
    </>
  )
}

function Steps({ steps }: { steps: RecipeStep[] }) {
  const { t } = useTranslation()
  if (!isArray(steps) || steps.length < 1) {
    return <span>{t('recipe-has-no-steps')}</span>
  }

  return (
    <>
      <h3>{t('recipe-steps')}</h3>
      <ol>
        {steps.map((step, index) => (
          <li key={`${step.message}-${index}`}>
            {step.message} {step?.parameters?.time ? `(${humanizeDuration(step.parameters.time * 1000)})` : ''}
          </li>
        ))}
      </ol>
    </>
  )
}

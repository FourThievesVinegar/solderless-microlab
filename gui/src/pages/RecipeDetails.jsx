import humanizeDuration from 'humanize-duration'
import { capitalize, get, isArray, isEmpty, reduce } from 'lodash'
import React, { useEffect, useState } from 'react'
import { useHistory, useParams } from 'react-router-dom'
import { Button } from 'semantic-ui-react'
import '../styles/app.css'
import { apiUrl } from '../utils'

export function RecipeDetails() {
  const [recipeDetails, setRecipeDetails] = useState({})
  const history = useHistory()
  const { recipeName } = useParams()

  // fetch recipe details, such as steps, ingredients, time
  useEffect(() => {
    fetch(apiUrl + 'recipe/' + recipeName)
      .then(response => response.json())
      .then(data => setRecipeDetails(data))
  }, [recipeName])

  const startRecipe = name => {
    fetch(apiUrl + 'start/' + name, {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => history.push('/status'))
  }

  const StartRecipeButton = () => {
    return (
      <Button
        color="purple"
        onClick={() => {
          startRecipe(recipeName)
          history.push('/status')
        }}>
        Start A Reaction Using This Recipe
      </Button>
    )
  }

  return (
    <section className="page recipe-details">
      <h1>{capitalize(recipeName)}</h1>
      <StartRecipeButton />

      {!isEmpty(recipeDetails) ? (
        <>
          <MaterialsNeeded materials={recipeDetails.materials} />
          <TimeNeeded steps={recipeDetails.steps} />
          <Steps steps={recipeDetails.steps} />
        </>
      ) : (
        <p>loading...</p>
      )}
      <StartRecipeButton />
    </section>
  )
}

function MaterialsNeeded({ materials }) {
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
    body = <span>No materials needed</span>
  }

  return (
    <>
      <h3>Materials Needed:</h3>
      {body}
    </>
  )
}

/**
 * total time? which steps are time sensitive and how long between them?
 * */
function TimeNeeded({ steps }) {
  if (!isArray(steps) || steps.length < 1) {
    return <></>
  }

  const waitTime = reduce(
    steps,
    (sum, step) => {
      return sum + reduce(
        step.tasks,
        (max, task) =>
          Math.max(get(task, 'parameters.time', 0), max),
        0,
      )
    },
    0,
  )

  function TimeNeededSection({ label, seconds }) {
    return (
      <p>
        <b>{`${label}: `}</b>
        <span>{humanizeDuration(seconds * 1000)}</span>
      </p>
    )
  }

  return (
    <>
      <h3>Time Needed:</h3>
      <TimeNeededSection label="Time needed for automated tasks" seconds={waitTime} />
    </>
  )
}

function Steps({ steps }) {
  if (!isArray(steps) || steps.length < 1) {
    return <span>No steps</span>
  }

  return (
    <>
      <h3>Steps:</h3>
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

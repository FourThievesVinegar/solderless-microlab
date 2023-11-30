import React, { useState, useEffect } from 'react'
import { Switch, Route } from 'react-router-dom'

import { Header } from './components/Header'
import { Home } from './pages/Home'
import { Recipes } from './pages/Recipes'
import { RecipeDetails } from './pages/RecipeDetails'
import { ReactionHistory } from './pages/ReactionHistory'
import { Tests } from './Tests'
import { Settings } from './pages/Settings'
import { Status } from './pages/Status'

import { getStatus } from './utils'

import './styles/app.css'

export function App() {
  const [status, setStatus] = useState()

  useEffect(() => {
    const interval = setInterval(() => {
      getStatus(setStatus)
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="lcd-wrapper">
      <Header>
        {status ?
          `${status?.step ? `${status?.step}: ` : ""}${status?.status} ${status?.temp ? `${status?.temp}C` : ""}` :
          "Waiting for control service"
        }
      </Header>
      <Switch>
        <Route exact path="/">
          <Home status={status} />
        </Route>

        <Route exact path="/recipes">
          <Recipes />
        </Route>

        <Route path="/recipes/:recipeName">
          <RecipeDetails />
        </Route>

        <Route path="/reaction-history">
          <ReactionHistory />
        </Route>

        <Route path="/tests">
          <Tests />
        </Route>

        <Route path="/settings">
          <Settings />
        </Route>

        <Route path="/status">
          <Status status={status} />
        </Route>
      </Switch>
    </div>
  )
}

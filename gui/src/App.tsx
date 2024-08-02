import React, { useState, useEffect, useContext } from 'react'
import { Switch, Route } from 'react-router-dom'

import { Header } from './components/Header'
import { Home } from './pages/Home'
import { Recipes } from './pages/Recipes'
import { RecipeDetails } from './pages/RecipeDetails'
import { Settings } from './pages/Settings'
import { Status } from './pages/Status'
import { Logs } from './pages/Logs'
import SettingsContext from './contexts/Settings'
import { SOUNDS, useAudio } from './hooks/useAudio'
import { getStatus } from './utils'
import { HardwareStatus } from './pages/HardwareStatus'

import './styles/app.css'
import './styles/4tv.scss'

export function App() {
  const [status, setStatus] = useState<any>()
  const { settings } = useContext(SettingsContext)
  const [errorPlaying, playErrorSound] = useAudio(SOUNDS.ERROR)
  const [completePlaying, playCompleteSound] = useAudio(SOUNDS.COMPLETE)
  const [promptPlaying, playPromptAudio] = useAudio(SOUNDS.PROMPT)

  const handleGetStatusError = () => {
    const mockStatus = {
      message: 'Service down',
      status: 'Waiting for control service',
      step: -1,
    }
    setStatus(mockStatus)
  }

  const updateStatusAndGetItAgain = (data: any) => {
    setStatus(data)

    setTimeout(() => {
      getStatus(updateStatusAndGetItAgain, handleGetStatusError)
    }, 2500)
  }

  useEffect(() => {
    getStatus(updateStatusAndGetItAgain, handleGetStatusError)
  }, [])

  useEffect(() => {
    if (status?.status === 'error' && !settings.muteErrorSound) {
      playErrorSound(true)
    } else if (status?.status === 'user_input' && !settings.muteUserInputSound) {
      playPromptAudio(true)
      const interval = setInterval(() => {
        if (!settings.muteUserInputSound) {
          playPromptAudio(true)
        }
      }, 30 * 1000)

      return () => clearInterval(interval)
    } else if (status?.status === 'complete' && !settings.muteCompletionSound) {
      playCompleteSound(true)
    }
  }, [status?.status, status?.step])

  return (
    <div className={`lcd-wrapper${settings.darkMode ? ' dark-mode' : ''}`}>
      <Header>
        {status
          ? `${status?.step ? `${status?.step}: ` : ''}${status?.status} ${
              typeof status?.temp === 'number' ? `${status?.temp.toFixed(2)}C` : ''
            }`
          : 'Waiting for control service'}
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

        <Route path="/settings">
          <Settings />
        </Route>

        <Route path="/status">
          <Status status={status} />
        </Route>

        <Route path="/hardwareStatus">
          <HardwareStatus status={status} />
        </Route>

        <Route path="/logs">
          <Logs />
        </Route>
      </Switch>
    </div>
  )
}

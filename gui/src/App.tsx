import React, { useState, useEffect, useContext } from 'react'
import { Switch, Route } from 'react-router-dom'

import { Header } from './components/Header'
import { HomePage } from './pages/HomePage'
import { RecipesPage } from './pages/RecipesPage'
import { RecipeDetails } from './pages/RecipeDetailsPage'
import { SettingsPage } from './pages/SettingsPage'
import { StatusPage } from './pages/StatusPage'
import { LogsPage } from './pages/LogsPage'
import SettingsContext from './contexts/Settings'
import { SOUNDS, useAudio } from './hooks/useAudio'
import { getStatus } from './utils'
import { HardwareStatusPage } from './pages/HardwareStatusPage'
import { MicrolabStatusResponse, MicrolabStatus } from './microlabTypes'
import { useTranslation } from 'react-i18next'

import './styles/app.css'
import './styles/4tv.scss'

export function App() {
  const { t } = useTranslation()
  const mockStatus = {
    message: t('backend-down'),
    status: MicrolabStatus.NO_BACKEND_RESPONSE,
    step: -1,
  }
  const [status, setStatus] = useState<MicrolabStatusResponse>(mockStatus)
  const { settings } = useContext(SettingsContext)
  const [errorPlaying, playErrorSound] = useAudio(SOUNDS.ERROR)
  const [completePlaying, playCompleteSound] = useAudio(SOUNDS.COMPLETE)
  const [promptPlaying, playPromptAudio] = useAudio(SOUNDS.PROMPT)

  const handleGetStatusError = () => {
    setStatus(mockStatus)
  }

  const updateStatusAndGetItAgain = (data: MicrolabStatusResponse) => {
    setStatus(data)

    setTimeout(() => {
      getStatus(updateStatusAndGetItAgain, handleGetStatusError)
    }, 2500)
  }

  useEffect(() => {
    getStatus(updateStatusAndGetItAgain, handleGetStatusError)
  }, [])

  useEffect(() => {
    if (status?.status === MicrolabStatus.ERROR && !settings.muteErrorSound) {
      playErrorSound(true)
    } else if (status?.status === MicrolabStatus.USER_INPUT && !settings.muteUserInputSound) {
      playPromptAudio(true)
      const interval = setInterval(() => {
        if (!settings.muteUserInputSound) {
          playPromptAudio(true)
        }
      }, 30 * 1000)

      return () => clearInterval(interval)
    } else if (status?.status === MicrolabStatus.COMPLETE && !settings.muteCompletionSound) {
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
          : t('waiting-for-backend')}
      </Header>
      <Switch>
        <Route exact path="/">
          <HomePage status={status} />
        </Route>

        <Route exact path="/recipes">
          <RecipesPage />
        </Route>

        <Route path="/recipes/:recipeName">
          <RecipeDetails />
        </Route>

        <Route path="/settings">
          <SettingsPage />
        </Route>

        <Route path="/status">
          <StatusPage status={status} />
        </Route>

        <Route path="/hardwareStatus">
          <HardwareStatusPage status={status} />
        </Route>

        <Route path="/logs">
          <LogsPage />
        </Route>
      </Switch>
    </div>
  )
}

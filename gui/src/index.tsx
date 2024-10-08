import React from 'react'
import { App } from './App'
import { BrowserRouter as Router } from 'react-router-dom'
import { createRoot } from 'react-dom/client'
import { SettingsProvider } from './contexts/Settings'
import './localization'

const container = document.getElementById('root')
//@ts-ignore
const root = createRoot(container)

root.render(
  <SettingsProvider>
    <Router>
      <App />
    </Router>
  </SettingsProvider>,
)

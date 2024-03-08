import React, { useState } from 'react'
import { useLocalStorage } from '@uidotdev/usehooks'

const SettingsContext = React.createContext()

const defaultSettings = {
  muteErrorSound: false,
  muteUserInputSound: false,
  muteCompletionSound: false,
  darkMode: true,
}

export const SettingsProvider = ({ children, settings }) => {
  const [currentSettings, setCurrentSettings] = useLocalStorage('settings', settings || defaultSettings)

  const updateSettings = values => {
    setCurrentSettings({ ...currentSettings, ...values })
  }

  return (
    <SettingsContext.Provider value={{ settings: currentSettings, updateSettings }}>
      {children}
    </SettingsContext.Provider>
  )
}

export const SettingsConsumer = SettingsContext.Consumer

export default SettingsContext

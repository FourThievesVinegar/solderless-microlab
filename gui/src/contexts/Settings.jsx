import React, { useState } from 'react'
import { useLocalStorage } from '@uidotdev/usehooks'
import { AUDIO_THEMES } from "../hooks/useAudio"

const SettingsContext = React.createContext()

const defaultSettings = {
  muteErrorSound: false,
  muteUserInputSound: false,
  muteCompletionSound: false,
  muteIntroSound: false,
  darkMode: true,
  audioTheme: AUDIO_THEMES.RAGE,
}

export const SettingsProvider = ({ children, settings }) => {
  const [currentSettings, setCurrentSettings] = useLocalStorage('settings', { defaultSettings, ...settings })

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

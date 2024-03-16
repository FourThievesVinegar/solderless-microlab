import React, { useEffect, useState } from 'react'
import { useLocalStorage } from '@uidotdev/usehooks'
import { AUDIO_THEMES } from '../hooks/useAudio'

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
  const [audioPlaybackAllowed, setAudioPlaybackAllowed] = useState(false)
  const [currentSettings, setCurrentSettings] = useLocalStorage('settings', { defaultSettings, ...settings })

  const updateSettings = values => {
    setCurrentSettings({ ...currentSettings, ...values })
  }
  useEffect(() => {
    // playing audio before the user interacts with the page throws an error,
    // so wait for interaction before allowing audio playback
    window.addEventListener('click', () => {
      setAudioPlaybackAllowed(true)
    })
  }, [])

  return (
    <SettingsContext.Provider value={{ settings: { ...currentSettings, audioPlaybackAllowed }, updateSettings }}>
      {children}
    </SettingsContext.Provider>
  )
}

export const SettingsConsumer = SettingsContext.Consumer

export default SettingsContext

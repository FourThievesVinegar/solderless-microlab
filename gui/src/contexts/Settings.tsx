import React, { useEffect, useState } from 'react'
import { useLocalStorage } from '@uidotdev/usehooks'
import { AUDIO_THEMES } from '../hooks/useAudio'

export type Settings = {
  muteErrorSound: boolean
  muteUserInputSound: boolean
  muteCompletionSound: boolean
  muteIntroSound: boolean
  darkMode: boolean
  audioTheme: string
}

export type SettingsContext = {
  settings: Settings & { audioPlaybackAllowed: boolean }
  updateSettings: (values: Partial<Settings>) => void
}

const defaultSettings = {
  muteErrorSound: false,
  muteUserInputSound: false,
  muteCompletionSound: false,
  muteIntroSound: false,
  darkMode: true,
  audioTheme: AUDIO_THEMES.RAGE,
}

const SettingsContext = React.createContext<SettingsContext>({
  settings: { ...defaultSettings, audioPlaybackAllowed: false },
  updateSettings: () => {},
})

export const SettingsProvider = ({ children, settings }: { children: any; settings?: Partial<Settings> }) => {
  const [audioPlaybackAllowed, setAudioPlaybackAllowed] = useState(false)
  const [currentSettings, setCurrentSettings] = useLocalStorage('settings', { ...defaultSettings, ...settings })

  const updateSettings = (values: Partial<Settings>) => {
    setCurrentSettings((currentSettings: Settings) => ({ ...defaultSettings, ...currentSettings, ...values }))
  }
  useEffect(() => {
    // playing audio before the user interacts with the page throws an error,
    // so wait for interaction before allowing audio playback
    window.addEventListener('click', () => {
      setAudioPlaybackAllowed(true)
    })
    // After the first page load the settings key in localstorage is always defined so
    // any new default settings never get set from the useLocalStorage initial value,
    // an empty update lets that happen
    updateSettings({})
  }, [])

  return (
    <SettingsContext.Provider value={{ settings: { ...currentSettings, audioPlaybackAllowed }, updateSettings }}>
      {children}
    </SettingsContext.Provider>
  )
}

export const SettingsConsumer = SettingsContext.Consumer

export default SettingsContext

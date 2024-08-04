import { useState, useEffect, useContext } from 'react'
import SettingsContext from '../contexts/Settings'

export const SOUNDS = {
  INTRO: 'intro',
  ERROR: 'error',
  COMPLETE: 'complete',
  PROMPT: 'prompt',
}

export const AUDIO_THEMES = {
  SIMPLE: 'simple',
  RAGE: 'rage',
}

const THEME_FORMATS = {
  [AUDIO_THEMES.RAGE]: 'mp3',
  [AUDIO_THEMES.SIMPLE]: 'wav',
}

const rootURL = process.env.PUBLIC_URL

export const useAudio = (type: string): [boolean, React.Dispatch<React.SetStateAction<boolean>>] => {
  const { settings } = useContext(SettingsContext)
  const theme = settings.audioTheme || AUDIO_THEMES.RAGE
  const fileUrl = `${rootURL}/audio/${theme}/${type}.${THEME_FORMATS[theme]}`
  const [audio, setAudio] = useState(() => new Audio(fileUrl))
  const [playing, setPlaying] = useState(false)

  useEffect(() => {
    if (settings.audioPlaybackAllowed) {
      audio.volume = settings.volume
      playing ? audio.play() : audio.pause()
    }
  }, [playing])

  useEffect(() => {
    audio.addEventListener('ended', () => setPlaying(false))
    return () => {
      audio.removeEventListener('ended', () => setPlaying(false))
    }
  }, [])

  return [playing, setPlaying]
}

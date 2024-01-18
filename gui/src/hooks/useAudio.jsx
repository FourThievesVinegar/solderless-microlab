import { useState, useEffect } from 'react'

export const useAudio = url => {
  const [audio, setAudio] = useState(() => new Audio(url), [])
  const [playing, setPlaying] = useState(false)

  useEffect(() => {
    playing ? audio.play() : audio.pause()
  }, [playing])

  useEffect(() => {
    audio.addEventListener('ended', () => setPlaying(false))
    return () => {
      audio.removeEventListener('ended', () => setPlaying(false))
    }
  }, [])

  return [playing, setPlaying]
}

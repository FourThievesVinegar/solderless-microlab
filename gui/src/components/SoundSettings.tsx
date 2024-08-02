import React, { ChangeEventHandler, useContext } from 'react'
import { Form, Checkbox, Dropdown } from 'semantic-ui-react'
import SettingsContext from '../contexts/Settings'
import { AUDIO_THEMES } from '../hooks/useAudio'
import './SoundSettings.scss'

export const SoundSettings = (props: any) => {
  const { settings, updateSettings } = useContext(SettingsContext)

  const audioThemeOptions = Object.keys(AUDIO_THEMES)?.map(theme => ({
    key: theme,
    //@ts-ignore
    value: AUDIO_THEMES[theme],
    //@ts-ignore
    text: AUDIO_THEMES[theme],
  }))

  const updateVolume: ChangeEventHandler<HTMLInputElement> = event => {
    updateSettings({ volume: Number(event.target.value) })
  }

  return (
    <Form>
      <h2>Sound Settings</h2>
      <div className="settings-block">
        <label>Soundscape: </label>
        <Dropdown
          placeholder="Select your audio theme"
          options={audioThemeOptions}
          value={settings.audioTheme}
          onChange={(event: any, data: any) => {
            updateSettings({ audioTheme: data.value })
          }}
        />
      </div>
      <div className="settings-block">
        <label>Volume: </label>
        <br />
        <input type="range" min="0" max="1" step="0.01" value={settings.volume} onChange={updateVolume} />
      </div>
      <div className="settings-block">
        <span>Play Sounds:</span>
        <Checkbox
          className="sound-setting-checkbox"
          label="On Error"
          checked={!settings.muteErrorSound}
          onChange={() => {
            updateSettings({ muteErrorSound: !settings.muteErrorSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label="Step Requires User Input"
          checked={!settings.muteUserInputSound}
          onChange={() => {
            updateSettings({ muteUserInputSound: !settings.muteUserInputSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label="On Recipe Completion"
          checked={!settings.muteCompletionSound}
          onChange={() => {
            updateSettings({ muteCompletionSound: !settings.muteCompletionSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label="On Recipe List Load (intro)"
          checked={!settings.muteIntroSound}
          onChange={() => {
            updateSettings({ muteIntroSound: !settings.muteIntroSound })
          }}
        />
      </div>
    </Form>
  )
}

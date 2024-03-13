import React, { useContext } from 'react'
import { Form, Checkbox, Dropdown } from 'semantic-ui-react'
import SettingsContext from '../contexts/Settings'
import { AUDIO_THEMES } from "../hooks/useAudio"
import './SoundSettings.scss'

export const SoundSettings = props => {
  const { settings, updateSettings } = useContext(SettingsContext)

  const audioThemeOptions = Object.keys(AUDIO_THEMES)?.map(theme => ({
    key: theme,
    value: AUDIO_THEMES[theme],
    text: AUDIO_THEMES[theme]
  }))

  return (
    <Form>
      <h2>Sound Settings</h2>
      <div>
        <label>Soundscape: </label>
        <Dropdown
          placeholder='Select your audio theme'
          options={audioThemeOptions}
          value={settings.audioTheme}
          onChange={(event, data) => { updateSettings({ audioTheme: data.value }) }}
        />

      </div>
      <div>
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
      </div>
    </Form>
  )
}

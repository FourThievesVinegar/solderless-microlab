import React, { ChangeEventHandler, useContext } from 'react'
import { Form, Checkbox, Dropdown } from 'semantic-ui-react'
import SettingsContext from '../contexts/Settings'
import { AUDIO_THEMES } from '../hooks/useAudio'
import { useTranslation } from 'react-i18next'
import './SoundSettings.scss'

export const SoundSettings = (props: any) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.SoundSettings' })
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
      <div className="settings-block">
        <label>{t('soundscape-label')}: </label>
        <Dropdown
          placeholder={t('select-audio-theme-placeholder')}
          options={audioThemeOptions}
          value={settings.audioTheme}
          onChange={(event: any, data: any) => {
            updateSettings({ audioTheme: data.value })
          }}
        />
      </div>
      <div className="settings-block">
        <label>{t('volume-label')}: </label>
        <br />
        <input type="range" min="0" max="1" step="0.01" value={settings.volume} onChange={updateVolume} />
      </div>
      <div className="settings-block">
        <span>{t('play-sounds-label')}:</span>
        <Checkbox
          className="sound-setting-checkbox"
          label={t('sound-on-error-label')}
          checked={!settings.muteErrorSound}
          onChange={() => {
            updateSettings({ muteErrorSound: !settings.muteErrorSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label={t('sound-requires-user-input-label')}
          checked={!settings.muteUserInputSound}
          onChange={() => {
            updateSettings({ muteUserInputSound: !settings.muteUserInputSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label={t('sound-on-recipe-completion-label')}
          checked={!settings.muteCompletionSound}
          onChange={() => {
            updateSettings({ muteCompletionSound: !settings.muteCompletionSound })
          }}
        />
        <Checkbox
          className="sound-setting-checkbox"
          label={t('sound-intro-label')}
          checked={!settings.muteIntroSound}
          onChange={() => {
            updateSettings({ muteIntroSound: !settings.muteIntroSound })
          }}
        />
      </div>
    </Form>
  )
}

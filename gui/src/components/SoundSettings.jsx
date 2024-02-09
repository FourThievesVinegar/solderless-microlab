import React, { useState, useEffect, useContext } from 'react'
import { Button, Input, Form, Checkbox, Label } from 'semantic-ui-react'
import SettingsContext from '../contexts/Settings'
import './SoundSettings.scss'

export const SoundSettings = props => {
  const { settings, updateSettings } = useContext(SettingsContext)

  return (
    <Form>
      <Label>Sound Settings</Label>
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

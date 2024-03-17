import React, { useReducer, useContext } from 'react'
import { ButtonGroup, Button, Icon } from 'semantic-ui-react';

import { ControllerHardwareConfig } from '../components/ControllerHardwareConfig'
import { LabHardwareConfig } from '../components/LabHardwareConfig'
import { LabConfigUpload } from '../components/LabConfigUpload'
import { ControllerConfigUpload } from '../components/ControllerConfigUpload'
import { SoundSettings } from '../components/SoundSettings'

import SettingsContext from '../contexts/Settings'

import './Settings.scss'

export function Settings() {
  // dummy counter to have components refetch data
  const [counter, updateCounter] = useReducer(x => x + 1, 0)

  const { settings, updateSettings } = useContext(SettingsContext)

  return (
    <div className="page settings-page">
      <h1>Settings</h1>
      <div className="settings-block">
        <ButtonGroup>
          <Button color="yellow" size="small" onClick={() => updateSettings({ darkMode: false })}>
            <Icon name="sun" />
          </Button>
          <Button color="purple" size="small" onClick={() => updateSettings({ darkMode: true })}>
            <Icon name="moon" />
          </Button>
        </ButtonGroup>
      </div>
      <div className="settings-block">
        <ControllerHardwareConfig refetch={counter} />
        <ControllerConfigUpload onUpload={updateCounter} />
      </div>
      <div className="settings-block">
        <LabHardwareConfig refetch={counter} />
        <LabConfigUpload onUpload={updateCounter} />
      </div>
      <div className="settings-block">
        <SoundSettings />
      </div>
    </div>
  )
}

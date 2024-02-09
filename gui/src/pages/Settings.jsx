import React, { useReducer } from 'react'
// import { Button, Icon, Menu, Segment } from 'semantic-ui-react';
import { ControllerHardwareConfig } from '../components/ControllerHardwareConfig'
import { LabHardwareConfig } from '../components/LabHardwareConfig'
import { LabConfigUpload } from '../components/LabConfigUpload'
import { ControllerConfigUpload } from '../components/ControllerConfigUpload'
import { SoundSettings } from '../components/SoundSettings'

import './Settings.scss'

export function Settings() {
  // dummy counter to have components refetch data
  const [counter, updateCounter] = useReducer(x => x + 1, 0)

  return (
    <div className="page settings-page">
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

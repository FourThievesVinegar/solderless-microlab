import React, { useReducer, useContext } from 'react'
import { ButtonGroup, Button, Divider, Icon } from 'semantic-ui-react'

import { ControllerHardwareConfig } from '../components/ControllerHardwareConfig'
import { LabHardwareConfig } from '../components/LabHardwareConfig'
import { LabConfigUpload } from '../components/LabConfigUpload'
import { ControllerConfigUpload } from '../components/ControllerConfigUpload'
import { SoundSettings } from '../components/SoundSettings'
import { ReloadHardware } from '../components/ReloadHardware'

import SettingsContext from '../contexts/Settings'
import { useTranslation } from 'react-i18next'

import './SettingsPage.scss'
import { LanguageSelector } from '../components/LanguageSelector'

export function SettingsPage() {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.SettingsPage' })
  // dummy counter to have components refetch data
  const [counter, updateCounter] = useReducer(x => x + 1, 0)

  const { updateSettings } = useContext(SettingsContext)

  return (
    <div className="page settings-page">
      <h1>{t('settings-page-header')}</h1>
      <div className="settings-block general-settings">
        <ButtonGroup>
          <Button color="yellow" size="small" onClick={() => updateSettings({ darkMode: false })}>
            <Icon name="sun" />
          </Button>
          <Button color="purple" size="small" onClick={() => updateSettings({ darkMode: true })}>
            <Icon name="moon" />
          </Button>
        </ButtonGroup>
        <LanguageSelector />
        <ReloadHardware displayMessage={true} />
      </div>
      <Divider />
      <div className="settings-block">
        <h2>{t('lab-hardware-config-header')}</h2>
        <ControllerHardwareConfig refetch={counter} />
        <ControllerConfigUpload onUpload={updateCounter} />
      </div>
      <Divider />
      <div className="settings-block">
        <h2>{t('controller-hardware-config-header')}</h2>
        <LabHardwareConfig refetch={counter} />
        <LabConfigUpload onUpload={updateCounter} />
      </div>
      <Divider />
      <div className="settings-block">
        <h2>{t('sound-config-header')}</h2>
        <SoundSettings />
      </div>
    </div>
  )
}

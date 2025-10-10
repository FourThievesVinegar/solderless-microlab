import React, { useState, useContext, useEffect } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Icon, Button, Menu, MenuItem } from 'semantic-ui-react'

import SettingsContext from '../contexts/Settings'
import { useTranslation } from 'react-i18next'

import './Header.scss'

export function Header(props: {
  children:
    | string
    | number
    | boolean
    | React.ReactElement<any, string | React.JSXElementConstructor<any>>
    | Iterable<React.ReactNode>
    | React.ReactPortal
    | null
    | undefined
}) {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.Header' })
  const history = useHistory()
  const { settings } = useContext(SettingsContext)

  const [showMenu, setShowMenu] = useState(false)
  const hideMenu = () => setShowMenu(false)

  const [showBackButton, setShowBackButton] = useState(false)

  useEffect(() => {
    if (window.location.pathname === '/') {
      setShowBackButton(false)
    } else {
      setShowBackButton(true)
    }
  }, [showMenu, window.location.pathname])

  return (
    <>
      <section className="microlab-header">
        <Menu>
          <Menu.Item
            className={`back-button${showBackButton ? '' : ' hidden'}`}
            icon
            onClick={() => {
              if (showMenu) {
                hideMenu()
              } else if (showBackButton) {
                history.goBack()
              }
            }}>
            {showBackButton && <Icon name={`chevron left`} inverted={settings.darkMode} />}
          </Menu.Item>

          <Menu.Item header className="header-content">
            {props.children}
          </Menu.Item>

          <Menu.Item icon position="right" as={Button} onClick={() => setShowMenu(!showMenu)}>
            <Icon name={showMenu ? 'close' : 'bars'} />
          </Menu.Item>
        </Menu>
      </section>
      <aside className={`main-menu ${showMenu ? 'active' : ''}`}>
        <h2>{t('main-menu')}</h2>
        <div className="button-list">
          <Button as={Link} color="blue" to="/hardwareStatus" onClick={hideMenu}>
            {t('status-button-text')}
          </Button>
          <Button as={Link} color="blue" to="/recipes" onClick={hideMenu}>
            {t('recipes-button-text')}
          </Button>
          <Button as={Link} color="blue" to="/settings" onClick={hideMenu}>
            {t('settings-button-text')}
          </Button>
          <Button as={Link} color="blue" to="/logs" onClick={hideMenu}>
            {t('logs-button-text')}
          </Button>
        </div>
      </aside>
    </>
  )
}

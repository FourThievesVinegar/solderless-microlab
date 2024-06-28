import React, { useState, useContext, useEffect } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Icon, Button, Menu } from 'semantic-ui-react'

import SettingsContext from '../contexts/Settings'

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
      <section>
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

          <Menu.Item header>{props.children}</Menu.Item>

          <Menu.Item icon position="right" as={Button} onClick={() => setShowMenu(!showMenu)}>
            <Icon name={showMenu ? 'close' : 'bars'} />
          </Menu.Item>
        </Menu>
      </section>
      <aside className={`main-menu ${showMenu ? 'active' : ''}`}>
        <h2>Main menu</h2>
        <div className="button-list">
          <Button as={Link} color="blue" to="/recipes" onClick={hideMenu}>
            Recipes
          </Button>
          <Button as={Link} color="blue" to="/settings" onClick={hideMenu}>
            Settings
          </Button>
          <Button as={Link} color="blue" to="/logs" onClick={hideMenu}>
            View Logs
          </Button>
        </div>
      </aside>
    </>
  )
}

import React, { useState, useContext } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Icon, Button, Menu } from 'semantic-ui-react'

import SettingsContext from '../contexts/Settings'

export function Header(props) {
  const history = useHistory()
  const { settings } = useContext(SettingsContext)

  const [showMenu, setShowMenu] = useState(false)

  const hideMenu = () => setShowMenu(false)

  return (
    <>
      <section>
        <Menu>
          <Menu.Item
            icon
            onClick={() => {
              history.goBack()
            }}
            disabled={window.location.pathname === '/'}>
            <Icon name={`chevron left`} inverted={settings.darkMode} />
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
          <Button as={Link} color="blue" to="/reaction-history" onClick={hideMenu}>
            Reaction History
          </Button>
          <Button as={Link} color="blue" to="/logs" onClick={hideMenu}>
            View Logs
          </Button>
        </div>
      </aside>
    </>
  )
}

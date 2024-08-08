import React, { useState } from 'react'
import { Button, Container, Grid } from 'semantic-ui-react'
import { useHistory } from 'react-router-dom'
import { StatusIcon } from '../components/StatusIcon'
import { ReloadHardware } from '../components/ReloadHardware'
import { MicrolabStatus, StatusEnum } from '../microlabTypes'

import './Status.scss'

export function HardwareStatus(props: { status: MicrolabStatus }) {
  const { status } = props
  const [loading, setLoading] = useState(false)
  const history = useHistory()

  const handleLogsButtonClick = () => {
    history.push('/logs')
    return
  }

  const handleRecipeButtonClick = () => {
    history.push('/status')
    return
  }

  const handleHardwareReloadClick = () => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
    }, 1000)
  }

  return (
    <section className="page status-page">
      <Grid divided className="status-page-grid">
        <Grid.Row columns={2}>
          <Grid.Column>
            <Container textAlign="center">
              <StatusIcon icon={status.icon ?? ''} />
              <p className="status-message">{loading ? 'Reloading Hardware...' : status.message}</p>
            </Container>
          </Grid.Column>
          <Grid.Column className="status-page-menu">
            <div className="button-list">
              {status.status === StatusEnum.IDLE && (
                <>
                  <p>Microlab is idle. </p>
                </>
              )}
              {(status.status === StatusEnum.RUNNING ||
                status.status === StatusEnum.COMPLETE ||
                status.status === StatusEnum.USER_INPUT ||
                status.status === StatusEnum.RECIPE_UNSUPPORTED) && (
                <>
                  <p>Microlab is running a recipe.</p>
                  <Button color="purple" onClick={() => handleRecipeButtonClick()}>
                    Go to Recipe
                  </Button>
                </>
              )}
              {status.status === StatusEnum.ERROR && (
                <>
                  <p>Error: {status.hardwareError}</p>
                  <Button color="purple" onClick={() => handleLogsButtonClick()}>
                    View Logs
                  </Button>
                </>
              )}
              {(status.status === StatusEnum.ERROR || status.status === StatusEnum.IDLE) && (
                <ReloadHardware onReload={handleHardwareReloadClick} />
              )}
            </div>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </section>
  )
}

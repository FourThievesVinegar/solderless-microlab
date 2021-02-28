import React, { useState, useEffect } from 'react'
import { Button, Container, Grid } from 'semantic-ui-react'

import { selectOption, stopRecipe } from '../utils'

export function Status(props) {
  const { status } = props
  const [loading, setLoading] = useState(false)

  const handleOptionButtonClick = option => {
    if (loading) return
    setLoading(true)
    selectOption(option)
  }

  const handleStopButtonClick = () => {
    if (window.confirm('Are you sure you want to stop?')) {
      stopRecipe()
      window.history.back()
    }
  }

  useEffect(() => {
    setLoading(false)
  }, [status])

  return (
    <section className="page status-page">
      {status ? (
        <Grid divided className="status-page-grid">
          <Grid.Row columns={2}>
            <Grid.Column>
              <Container>
                <p className="status-message">{status.message}</p>
              </Container>
            </Grid.Column>
            <Grid.Column className="status-page-menu">
              <div className="button-list">
                {status.options.map(x => (
                  <Button color="green" key={x} onClick={() => handleOptionButtonClick(x)} loading={loading}>
                    {x}
                  </Button>
                ))}
                <Button color="red" onClick={() => handleStopButtonClick()}>
                  Stop Reaction
                </Button>
              </div>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      ) : (
        <p>Loading...</p>
      )}
    </section>
  )
}

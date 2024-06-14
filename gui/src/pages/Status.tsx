import React, { useState, useEffect } from 'react'
import humanizeDuration from 'humanize-duration'
import { Button, Container, Grid } from 'semantic-ui-react'
import { useHistory } from 'react-router-dom'
import { StatusIcon } from '../components/StatusIcon'
import { selectOption, stopRecipe } from '../utils'

import './Status.scss'

export function Status(props: {
  status: { status: string; step: number; stepCompletionTime: Date; icon: string; message: string; options: string[] }
}) {
  const { status } = props
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(-1)
  const [stepTime, setStepTime] = useState<Date>()
  const history = useHistory()

  const handleOptionButtonClick = (option: string) => {
    if (loading) return
    setLoading(true)
    selectOption(option)
  }

  const handleStopButtonClick = () => {
    if (status.status === 'complete') {
      stopRecipe()
      history.push('/')
      return
    }
    if (window.confirm('Are you sure you want to stop?')) {
      stopRecipe()
      history.push('/recipes')
    }
  }

  useEffect(() => {
    setLoading(false)
    if (status && status.step !== currentStep) {
      setCurrentStep(status.step)
      if (status.stepCompletionTime) {
        setStepTime(new Date(status.stepCompletionTime))
        return
      }
      setStepTime(undefined)
    }
  }, [status])

  return (
    <section className="page status-page">
      {status ? (
        <Grid divided className="status-page-grid">
          <Grid.Row columns={2}>
            <Grid.Column>
              <Container textAlign="center">
                <StatusIcon icon={status.icon} />
                <p className="status-message">{status.message}</p>
                {stepTime && (
                  //@ts-ignore
                  <p className="status-message">{`${humanizeDuration(stepTime - new Date(), { round: true })}`}</p>
                )}
              </Container>
            </Grid.Column>
            <Grid.Column className="status-page-menu">
              <div className="button-list">
                {status.options.map(x => (
                  <Button color="purple" key={x} onClick={() => handleOptionButtonClick(x)} loading={loading}>
                    {x}
                  </Button>
                ))}
                {(status.status === 'running' ||
                  status.status === 'user_input' ||
                  status.status === 'error' ||
                  status.status === 'recipe_unsupported') && (
                  <Button color="yellow" onClick={() => handleStopButtonClick()}>
                    Stop Reaction
                  </Button>
                )}
                {status.status === 'complete' && (
                  <Button color="purple" onClick={() => handleStopButtonClick()}>
                    Finish Reaction
                  </Button>
                )}
                {status.status === 'idle' && (
                  <>
                    <p>Waiting on backend... </p>
                    <Button color="yellow" onClick={() => handleStopButtonClick()}>
                      Go Back
                    </Button>
                  </>
                )}
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

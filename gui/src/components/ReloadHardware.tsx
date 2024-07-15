import React, { useState } from 'react'
import { reloadHardware } from '../utils'
import { Button, Form } from 'semantic-ui-react'

export const ReloadHardware = (props: { onReload?: () => void; displayMessage?: boolean }) => {
  const { onReload, displayMessage } = props
  const [message, setMessage] = useState('')

  const handleFormSubmit = () => {
    setMessage('Setting new configuration...')
    onReload?.()
    reloadHardware()
      .then(data => {
        if (data.response === 'ok') {
          setMessage('Hardware loaded successfully.')
          setTimeout(() => {
            setMessage('')
          }, 1000 * 10)
        } else {
          setMessage(`Loading hardware failed: "${data.message}"`)
        }
      })
      .catch(() => {
        setMessage('Loading hardware failed.')
      })
  }

  return (
    <Form>
      <Button type="submit" onClick={handleFormSubmit}>
        Reload Hardware
      </Button>
      <br />
      {displayMessage && message}
    </Form>
  )
}

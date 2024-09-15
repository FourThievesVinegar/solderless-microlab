import React, { useState } from 'react'
import { reloadHardware } from '../utils'
import { Button, Form } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

export const ReloadHardware = (props: { onReload?: () => void; displayMessage?: boolean }) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.ReloadHardware' })
  const { onReload, displayMessage } = props
  const [message, setMessage] = useState('')

  const handleFormSubmit = () => {
    setMessage(t('reloading-waiting-for-response-message'))
    onReload?.()
    reloadHardware()
      .then(data => {
        if (data.response === 'ok') {
          setMessage(t('reload-successful'))
          setTimeout(() => {
            setMessage('')
          }, 1000 * 10)
        } else {
          setMessage(t('reload-failed-with-message', { message: data.message }))
        }
      })
      .catch(() => {
        setMessage(t('reload-failed-generic'))
      })
  }

  return (
    <Form>
      <Button type="submit" onClick={handleFormSubmit}>
        {t('reload-button-text')}
      </Button>
      {message.length > 0 && displayMessage && <p className="hardware-reload-message">{message}</p>}
    </Form>
  )
}

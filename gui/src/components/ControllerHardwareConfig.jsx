import React, { useState, useEffect } from 'react'
import {
  setControllerHardware,
  listControllerHardware,
  getControllerHardware,
  downloadControllerConfig,
} from '../utils'
import { Button, Form, Dropdown } from 'semantic-ui-react'

export const ControllerHardwareConfig = props => {
  const { refetch } = props
  const [hardwareOptions, setHardwareOptions] = useState()
  const [selection, setSelection] = useState()
  const [loading, setLoading] = useState(true)
  const [startingValue, setStartingValue] = useState()

  const [message, setMessage] = useState('')

  const reloadData = async () => {
    const currentValue = (await getControllerHardware()).controllerHardware
    setSelection(currentValue)
    setStartingValue(currentValue)
    setHardwareOptions(await listControllerHardware())
    setLoading(false)
  }

  useEffect(() => {
    reloadData()
  }, [refetch])

  const selectionChanged = (event, data) => {
    setSelection(data.value)
  }

  const handleFormSubmit = (event, data) => {
    setMessage('Setting new configuration...')
    setControllerHardware(selection)
      .then(data => {
        if (data.response === 'ok') {
          setMessage('Controller configuration changed successfully.')
          setTimeout(() => {
            setMessage('')
          }, 1000 * 10)
        } else {
          setMessage(`Configuring controller failed: "${data.message}"`)
        }
        reloadData()
      })
      .catch(() => {
        setMessage('Configuring controller failed.')
      })
  }

  return (
    <Form>
      <h2>Microlab Controller</h2>
      <Dropdown
        selection
        loading={loading}
        text={selection}
        value={selection}
        options={hardwareOptions?.sort().map(a => ({ key: a, text: a, value: a }))}
        onChange={selectionChanged}
      />
      {startingValue !== selection ? (
        <Button type="submit" onClick={handleFormSubmit}>
          Save
        </Button>
      ) : (
        <></>
      )}
      {startingValue !== selection && (
        <Button className="cancel-button" onClick={() => setSelection(startingValue)}>
          X
        </Button>
      )}
      {startingValue === selection && (
        <Button className="cancel-button" onClick={() => downloadControllerConfig(selection)}>
          Download
        </Button>
      )}
      <br />
      {message}
    </Form>
  )
}

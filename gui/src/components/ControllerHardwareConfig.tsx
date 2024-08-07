import React, { useState, useEffect } from 'react'
import {
  setControllerHardware,
  listControllerHardware,
  getControllerHardware,
  downloadControllerConfig,
} from '../utils'
import { Button, Form, Dropdown } from 'semantic-ui-react'

export const ControllerHardwareConfig = (props: { refetch: any }) => {
  const { refetch } = props
  const [hardwareOptions, setHardwareOptions] = useState<undefined | string[]>()
  const [selection, setSelection] = useState<string>()
  const [loading, setLoading] = useState(true)
  const [startingValue, setStartingValue] = useState<string>()

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

  const selectionChanged = (event: any, data: any) => {
    setSelection(data.value)
  }

  const handleFormSubmit = (event: any, data: any) => {
    if (!selection) {
      setMessage('Failed, no configuration is selected.')
      return
    }
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
      <h2>MicroLab Controller</h2>
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
      {selection && startingValue === selection && (
        <Button className="cancel-button" onClick={() => downloadControllerConfig(selection)}>
          Download
        </Button>
      )}
      <br />
      {message}
    </Form>
  )
}

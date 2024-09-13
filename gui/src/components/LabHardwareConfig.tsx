import React, { useState, useEffect } from 'react'
import { setLabHardware, listLabHardware, getLabHardware, downloadLabConfig } from '../utils'
import { Button, Form, Dropdown } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

export const LabHardwareConfig = (props: { refetch: any }) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.LabHardwareConfig' })
  const { refetch } = props
  const [hardwareOptions, setHardwareOptions] = useState<undefined | string[]>()
  const [selection, setSelection] = useState<string>()
  const [loading, setLoading] = useState(true)
  const [startingValue, setStartingValue] = useState<string>()

  const [message, setMessage] = useState('')

  const reloadData = async () => {
    const currentValue = (await getLabHardware()).labHardware
    setSelection(currentValue)
    setStartingValue(currentValue)
    setHardwareOptions(await listLabHardware())
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
      setMessage(t('failed-no-selected-config'))
      return
    }
    setMessage(t('setting-new-config-waiting-message'))
    setLabHardware(selection)
      .then(data => {
        if (data.response === 'ok') {
          setMessage(t('config-changed-successfully'))
          setTimeout(() => {
            setMessage('')
          }, 1000 * 10)
        } else {
          setMessage(t('failed-config-change-request', { msg: data.message }))
        }
        reloadData()
      })
      .catch(() => {
        setMessage(t('failed-generic'))
      })
  }

  return (
    <Form>
      <h2>{t('header')}</h2>
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
          {t('save', {})}
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
        <Button className="cancel-button" onClick={() => downloadLabConfig(selection)}>
          {t('download')}
        </Button>
      )}
      <br />
      {message}
    </Form>
  )
}

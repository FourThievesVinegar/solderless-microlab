import React, { useState } from 'react'
import { uploadControllerConfig } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

export const ControllerConfigUpload = (props: { onUpload: () => void }) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.ControllerConfigUpload' })
  const { onUpload } = props
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<File | undefined>()

  const fileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handleFileUpload = () => {
    setMessage(t('uploading'))
    if (!file) {
      setMessage(t('upload-failed-no-file'))
      return
    }
    uploadControllerConfig(file)
      .then(() => {
        setMessage(t('upload-success'))
        onUpload()
      })
      .catch(() => {
        setMessage(t('upload-failed'))
      })
  }

  return (
    <Form onSubmit={handleFileUpload} encType="multipart/form-data">
      {message}
      <Input type="file" id="File" onChange={fileChange} />
      <Button type="submit">{t('upload-button-text')}</Button>
    </Form>
  )
}

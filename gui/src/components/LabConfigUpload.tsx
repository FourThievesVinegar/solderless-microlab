import React, { useState } from 'react'
import { uploadLabConfig } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

export const LabConfigUpload = (props: { onUpload: () => void }) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.LabConfigUpload' })
  const { onUpload } = props
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<File>()

  const fileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handleFileUpload = () => {
    if (file) {
      setMessage(t('upload-waiting-message'))
      uploadLabConfig(file)
        .then(() => {
          setMessage(t('upload-successful'))
          onUpload()
        })
        .catch(() => {
          setMessage(t('failed-generic'))
        })
    }
  }

  return (
    <Form onSubmit={handleFileUpload} encType="multipart/form-data">
      {message}
      <Input type="file" id="File" onChange={fileChange} />
      <Button type="submit">{t('upload-button-text')}</Button>
    </Form>
  )
}

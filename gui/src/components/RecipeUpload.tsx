import React, { useState } from 'react'
import { uploadRecipe } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'
import { useTranslation } from 'react-i18next'

export const RecipeUpload = ({ onUpload }: { onUpload?: () => void }) => {
  const { t } = useTranslation(undefined, { keyPrefix: 'components.RecipeUpload' })
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<File>()

  const fileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handleFileUpload = () => {
    if (!file) {
      setMessage(t('failed-no-recipe-selected'))
      return
    }
    setMessage(t('upload-waiting-message'))
    uploadRecipe(file)
      .then(response => {
        if (response.response === 'ok') {
          setMessage(t('upload-successful'))
          onUpload?.()
        } else if (response.response === 'error') {
          setMessage(response.message ?? t('upload-failed-generic'))
        }
      })
      .catch(() => {
        setMessage(t('upload-failed-generic'))
      })
  }

  return (
    <Form onSubmit={handleFileUpload} encType="multipart/form-data">
      <p style={{ whiteSpace: 'pre-wrap' }}>{message}</p>
      <Input type="file" id="File" onChange={fileChange} />
      <Button color="purple" type="submit">
        {t('upload-button-text')}
      </Button>
    </Form>
  )
}

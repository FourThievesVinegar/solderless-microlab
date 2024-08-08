import React, { useState } from 'react'
import { uploadControllerConfig } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const ControllerConfigUpload = (props: { onUpload: () => void }) => {
  const { onUpload } = props
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<File | undefined>()

  const fileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handleFileUpload = () => {
    setMessage('Uploading config...')
    if (!file) {
      setMessage('Failed, no file attached.')
      return
    }
    uploadControllerConfig(file)
      .then(() => {
        setMessage('Config upload successful.')
        onUpload()
      })
      .catch(() => {
        setMessage('Config upload failed.')
      })
  }

  return (
    <Form onSubmit={handleFileUpload} encType="multipart/form-data">
      {message}
      <Input type="file" id="File" onChange={fileChange} />
      <Button type="submit">Upload new controller config</Button>
    </Form>
  )
}

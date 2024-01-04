import React, { useState } from 'react'
import { uploadControllerConfig } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const ControllerConfigUpload = props => {
  const { onUpload } = props
  const [message, setMessage] = useState('')

  const [file, setFile] = useState()

  const fileChange = event => {
    setFile(event.target.files[0])
  }

  const handleFileUpload = () => {
    setMessage('Uploading config...')
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

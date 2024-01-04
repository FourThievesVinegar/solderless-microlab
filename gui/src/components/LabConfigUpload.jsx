import React, { useState } from 'react'
import { uploadLabConfig } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const LabConfigUpload = props => {
  const { onUpload } = props
  const [message, setMessage] = useState('')

  const [file, setFile] = useState()

  const fileChange = event => {
    setFile(event.target.files[0])
  }

  const handleFileUpload = () => {
    setMessage('Uploading config...')
    uploadLabConfig(file)
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
      <Button type="submit">Upload new lab config</Button>
    </Form>
  )
}

import React, { useState } from 'react'
import { uploadRecipe } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const RecipeUpload = () => {
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<any>()

  const fileChange = (event: any) => {
    setFile(event.target.files[0])
  }

  const handleFileUpload = () => {
    setMessage('Uploading recipe...')
    uploadRecipe(file)
      .then(() => {
        setMessage('Recipe upload successful.')
      })
      .catch(() => {
        setMessage('Recipe upload failed.')
      })
  }

  return (
    <Form onSubmit={handleFileUpload} encType="multipart/form-data">
      {message}
      <Input type="file" id="File" onChange={fileChange} />
      <Button color="purple" type="submit">
        Upload
      </Button>
    </Form>
  )
}

import React, { useState } from 'react'
import { uploadRecipe } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const RecipeUpload = ({ onUpload }: { onUpload?: () => void }) => {
  const [message, setMessage] = useState('')

  const [file, setFile] = useState<File>()

  const fileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handleFileUpload = () => {
    if (!file) {
      setMessage('Failed, no recipe selected to upload.')
      return
    }
    setMessage('Uploading recipe...')
    uploadRecipe(file)
      .then(() => {
        setMessage('Recipe upload successful.')
        onUpload?.()
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

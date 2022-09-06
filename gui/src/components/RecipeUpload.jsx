import React, { useState } from 'react'
import { uploadRecipe } from '../utils'
import { Button, Input, Form } from 'semantic-ui-react'

export const RecipeUpload = () => {
  const [file, setFile] = useState();

  const fileChange = (event) => {
    setFile( event.target.files[0] );
  };

  return(
  <Form onSubmit={() => uploadRecipe(file)} encType = "multipart/form-data">
      <Input type="file" id="File" onChange={fileChange} />
      <Button type="submit">Upload</Button>
  </Form>)
}

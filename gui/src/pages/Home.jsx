import React from 'react'
import { Link } from 'react-router-dom'
import { Button, Grid } from 'semantic-ui-react'

import Logo from '../assets/logo.svg'

export function Home(props) {
  const { status } = props

  return (
    <div className="home-page page">
      <Grid>
        <Grid.Row columns={2}>
          <Grid.Column>
            <img src={Logo} alt="Four Thieves Vinegar Logo" style={{ width: '80%', paddingTop: '2%' }} />
            <p>Four Thieves Vinegar Microlab</p>
          </Grid.Column>
          <Grid.Column className="home-page-menu">
            <div className="button-list">
              {status && status.recipe ? (
                //if there's a recipe in progress, give a link to see its status
                //if not, offer option to start reaction
                <div>
                  <p>{status.recipe} reaction in progress.</p>
                  <Button color="green" as={Link} to="/status">
                    Resume {status.recipe.toUpperCase()} Reaction
                    {/* maybe this would be a good place to preview next step? */}
                  </Button>
                  <Button as={Link} to="/recipes">
                    View Recipes
                  </Button>
                </div>
              ) : (
                <Button color="green" as={Link} to="/recipes">
                  View Recipes
                </Button>
              )}
            </div>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </div>
  )
}

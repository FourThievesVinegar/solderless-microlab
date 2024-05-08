import React from 'react'
import { Link } from 'react-router-dom'
import { Button, Grid } from 'semantic-ui-react'
import { LogoContainer } from '../components/LogoContainer'

import './Home.scss'

export function Home(props: { status: any }) {
  const { status } = props

  return (
    <div className="home-page page">
      <Grid style={{ height: '100%' }}>
        <Grid.Row columns={2} style={{ height: '100%' }}>
          <Grid.Column style={{ height: '100%' }}>
            <LogoContainer />
            <p>Four Thieves Vinegar MicroLab</p>
          </Grid.Column>
          <Grid.Column className="home-page-menu">
            <div className="button-list">
              {status && status.recipe ? (
                //if there's a recipe in progress, give a link to see its status
                //if not, offer option to start reaction
                <div>
                  <p>{status.recipe} reaction in progress.</p>
                  <Button color="purple" as={Link} to="/status">
                    Resume {status.recipe.toUpperCase()} Reaction
                    {/* maybe this would be a good place to preview next step? */}
                  </Button>
                  <Button as={Link} to="/recipes">
                    View Recipes
                  </Button>
                </div>
              ) : (
                <Button color="purple" as={Link} to="/recipes">
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

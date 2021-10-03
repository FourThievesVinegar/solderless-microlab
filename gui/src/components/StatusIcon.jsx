import React from 'react'

import { LogoSpinner } from './LogoSpinner'

import './StatusIcon.scss'

import looking from '../assets/looking.svg'
import emptySyringe from '../assets/syringe_empty.svg'
import syringe from '../assets/syringe.svg'
import temperature from '../assets/temperature.svg'
import reactionChamber from '../assets/reaction_chamber.svg'
import reactionComplete from '../assets/reaction_complete.svg'

export const StatusIcon = ({ icon }) => {
  let iconImage

  switch (icon) {
    case 'reaction_chamber':
      iconImage = reactionChamber
      break
    case 'load_syringe':
      iconImage = emptySyringe
      break
    case 'inspect':
      iconImage = looking
      break
    case 'dispensing':
      iconImage = syringe
      break
    case 'temperature':
      iconImage = temperature
      break
    case 'reaction_complete':
      iconImage = reactionComplete
      break
  }

  if (icon) {
    return (
      <div className="status-icon-container">
        <img className="status-icon" src={iconImage} />
      </div>
    )
  }

  return (
    <div className="status-icon-container">
      <LogoSpinner />
    </div>
  )
}

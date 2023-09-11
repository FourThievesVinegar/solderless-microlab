import React from 'react'

import { LogoSpinner } from './LogoSpinner'

import './StatusIcon.scss'

import complete from '../assets/step-icons/complete.svg'
import cooling from '../assets/step-icons/cooling.svg'
import crystalisation from '../assets/step-icons/crystalisation.svg'
import dry from '../assets/step-icons/dry.svg'
import filter from '../assets/step-icons/filter.svg'
import heating from '../assets/step-icons/heating.svg'
import humanTask from '../assets/step-icons/human-task.png'
import loadSyringe from '../assets/step-icons/load-syringe.svg'   // There are two variants of this with hands in the icon
import looking from '../assets/step-icons/looking-CC-muhammad-be.svg'
import maintainCool from '../assets/step-icons/maintain-cool.svg'
import maintainHeat from '../assets/step-icons/maintain-heat.svg'
import putIngredientInReactionChamber from '../assets/step-icons/put-ingredient-in-reaction-chamber.svg'
import rinse from '../assets/step-icons/rinse.svg'
import setUpCooling from '../assets/step-icons/set-up-cooling.svg'
import setUpHeating from '../assets/step-icons/set-up-heating.svg'
import stirring from '../assets/step-icons/stirring.svg'
import syringeDispensing from '../assets/step-icons/syringe-dispense.svg'

export const StatusIcon = ({ icon }) => {
  let iconImage

  switch (icon) {
    case 'reaction_complete':
      iconImage = complete
      break
    case 'cooling':
      iconImage = cooling
      break
    case 'crystalisation':
      iconImage = crystalisation
      break
    case 'dispensing':
      iconImage = syringeDispensing
      break
    case 'dry':
      iconImage = dry
      break
    case 'filter':
      iconImage = filter
      break
    case 'heating':
      iconImage = heating
      break
    case 'human_task':
      iconImage = humanTask
      break
    case 'inspect':
      iconImage = looking
      break
    case 'load_syringe':
      iconImage = loadSyringe
      break
    case 'maintain_cool':
      iconImage = maintainCool
      break
    case 'maintain_heat':
      iconImage = maintainHeat
      break
    case 'reaction_chamber':  // Possibly deprecated?
      iconImage = putIngredientInReactionChamber
      break
    case 'rinse':
      iconImage = rinse
      break
    case 'set_up_cooling':
      iconImage = setUpCooling
      break
    case 'set_up_heating':
      iconImage = setUpHeating
      break
    case 'stirring':
      iconImage = stirring
      break
    case 'temperature': // This should be deprecated for more precise icons
      iconImage = setUpHeating
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

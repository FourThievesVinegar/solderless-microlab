import React from 'react'

//import './LogoContainer.scss'

import LogoBurst from '../assets/logo-burst.svg'
import LogoBorder from '../assets/logo-border.svg'
import LogoHead from '../assets/logo-head.svg'

export const LogoContainer = () => (
  <div className="logo-container">
    <img src={LogoBurst} alt="Four Thieves Vinegar Logo" />
    <img src={LogoBorder} alt="Four Thieves Vinegar Logo" />
    <img src={LogoHead} alt="Four Thieves Vinegar Logo" />
  </div>
)

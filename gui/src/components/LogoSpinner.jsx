import React from 'react'

import './LogoSpinner.scss'

import LogoBurst from '../assets/logo-burst.svg'
import LogoBorder from '../assets/logo-border.svg'
import LogoHead from '../assets/logo-head.svg'

export const LogoSpinner = () => (
  <div className="logo-spinner">
    <img className="logo-head" src={LogoHead} alt="Four Thieves Vinegar Logo" />
    <img className="logo-burst" src={LogoBurst} alt="" />
    <img className="logo-border" src={LogoBorder} alt="" />
  </div>
)

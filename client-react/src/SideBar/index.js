import React from 'react'
import AppLink from '../SharedComponents/AppLink'

import './style.scss'

const SideBar = () => {
  return (
    <div id="sidebar">
      <AppLink href="/">Map</AppLink>
      <AppLink href="/charts">Charts</AppLink>
      <AppLink href="/about">About</AppLink>
    </div>
  )
}

export default SideBar

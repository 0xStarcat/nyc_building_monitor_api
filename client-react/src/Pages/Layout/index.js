import React from 'react'
import SideBar from '../../SideBar'

import './style.scss'

const MapPage = props => {
  return (
    <div id="pageLayout">
      <SideBar />
      <div id="sidebarGap" />
      <div id="mainContent">{props.children}</div>
    </div>
  )
}

export default MapPage

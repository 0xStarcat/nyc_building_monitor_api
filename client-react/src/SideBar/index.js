import React from 'react'
import { connect } from 'react'
import AppLink from '../SharedComponents/AppLink'
import SelectedLayer from './SelectedLayer'

import { deactivateSideBar } from '../Store/AppState/actions'

import './style.scss'

const SideBar = props => {
  const storeStyle = {
    transform: props.appState.sidebarActive ? 'translateX(0)' : 'translateX(-500px)'
  }

  const collapseSidebar = () => {
    props.dispatch(deactivateSideBar())
  }

  return (
    <div id="sidebar" style={storeStyle}>
      <button className="sidebar-button" id="sidebar-collapse" onClick={collapseSidebar}>
        X collapse
      </button>
      <SelectedLayer selectedLayer={props.appState.selectedLayer} />
    </div>
  )
}

export default SideBar

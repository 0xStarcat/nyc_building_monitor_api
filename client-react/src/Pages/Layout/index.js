import React from 'react'
import { connect } from 'react-redux'
import SideBar from '../../SideBar'

import './style.scss'

const Layout = props => {
  return (
    <div id="pageLayout">
      <SideBar selectedLayer={props.selectedLayer} />
      <div id="sidebarGap" />
      <div id="mainContent">{props.children}</div>
    </div>
  )
}

const mapStateToProps = state => {
  return {
    selectedLayer: state.appState.selectedLayer
  }
}
export default connect(mapStateToProps)(Layout)

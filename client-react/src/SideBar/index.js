import React from 'react'
import { connect } from 'react'
import AppLink from '../SharedComponents/AppLink'
import SelectedLayer from './SelectedLayer'
import './style.scss'

const SideBar = props => {
  return (
    <div id="sidebar">
      <SelectedLayer selectedLayer={props.selectedLayer} />
      <AppLink href="/">Map</AppLink>
      <AppLink href="/about">About</AppLink>
    </div>
  )
}

export default SideBar

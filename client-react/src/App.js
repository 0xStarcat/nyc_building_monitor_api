import React, { Component } from 'react'
import { connect } from 'react-redux'
import SideBar from './SideBar'
import MapPage from './Pages/MapPage'
import ChartPage from './Pages/ChartPage'
import AboutPage from './Pages/AboutPage'
import Loading from './SharedComponents/Loading'
import { readCensusTracts } from './Store/CensusTracts/actions'
import { readNeighborhoods } from './Store/Neighborhoods/actions'

import { history } from './Store/store'
import { Router, Switch, Route } from 'react-router'

import './App.scss'

class App extends Component {
  componentWillMount() {
    this.props.dispatch(readCensusTracts())
    // this.props.dispatch(readNeighborhoods())
  }

  render() {
    return (
      <div className="App">
        <Router history={history}>
          <Switch>
            <Route exact path="/" render={routeProps => <MapPage store={this.props.store} />} />
            <Route exact path="/charts" render={routeProps => <ChartPage store={this.props.store} />} />
            <Route exact path="/about" render={routeProps => <AboutPage />} />
          </Switch>
        </Router>
      </div>
    )
  }
}

const mapStateToProps = state => {
  return {
    store: state
  }
}

export default connect(
  mapStateToProps,
  null
)(App)

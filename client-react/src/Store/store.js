import { createStore, applyMiddleware, compose } from 'redux'

import thunk from 'redux-thunk'
import createHistory from 'history/createBrowserHistory'

import appReducer from './rootReducer'

export const history = createHistory()
const initialState = {}
const enhancers = []
const middleware = [thunk]

if (process.env.NODE_ENV === 'development') {
  const devToolsExtension = window.devToolsExtension

  if (typeof devToolsExtension === 'function') {
    enhancers.push(devToolsExtension())
  }
}

const composedEnhancers = compose(
  applyMiddleware(...middleware),
  ...enhancers
)

const store = createStore(appReducer, initialState, composedEnhancers)

export default store

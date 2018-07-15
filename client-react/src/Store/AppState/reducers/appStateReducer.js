import * as appStateActions from '../actions'

export const initialState = {
  allLayersLoaded: false
}

export const appStateReducer = (appState = Object.freeze(initialState), action = { data: [] }) => {
  switch (action.type) {
    case appStateActions.HANDLE_ALL_LAYERS_LOADED: {
      console.log('hi')
      return { ...appState, allLayersLoaded: true }
    }

    default:
      return appState
  }
}

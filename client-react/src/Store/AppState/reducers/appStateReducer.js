import * as appStateActions from '../actions'

export const initialState = {
  allLayersLoaded: false,
  selectedLayer: null
}

export const appStateReducer = (appState = Object.freeze(initialState), action = { data: [] }) => {
  switch (action.type) {
    case appStateActions.HANDLE_ALL_LAYERS_LOADED: {
      return { ...appState, allLayersLoaded: true }
    }
    case appStateActions.HANDLE_UPDATE_SELECTED_LAYER: {
      return { ...appState, selectedLayer: action.data }
    }

    default:
      return appState
  }
}

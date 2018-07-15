export const HANDLE_ALL_LAYERS_LOADED = 'HANDLE_ALL_LAYERS_LOADED'
export const HANDLE_UPDATE_SELECTED_LAYER = 'HANDLE_UPDATE_SELECTED_LAYER'

export const handleAllLayersLoaded = event => ({
  type: HANDLE_ALL_LAYERS_LOADED
})

export const handleUpdateSelectedLayer = event => ({
  type: HANDLE_UPDATE_SELECTED_LAYER,
  data: event
})

export const allLayersLoaded = () => dispatch => {
  dispatch(handleAllLayersLoaded())
}

export const updateSelectedLayer = () => dispatch => {
  dispatch(handleUpdateSelectedLayer())
}

export const HANDLE_ALL_LAYERS_LOADED = 'HANDLE_ALL_LAYERS_LOADED'

export const handleAllLayersLoaded = event => ({
  type: HANDLE_ALL_LAYERS_LOADED,
  data: event
})

export const allLayersLoaded = () => dispatch => {
  dispatch(handleAllLayersLoaded())
}

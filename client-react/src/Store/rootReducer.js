import { combineReducers } from 'redux'

import { censusTractsReducer } from './CensusTracts/reducers/censusTractsReducer'
import { neighborhoodsReducer } from './Neighborhoods/reducers/neighborhoodsReducer'

export default combineReducers({
  censusTracts: censusTractsReducer,
  neighborhoods: neighborhoodsReducer
})

import { UPDATE_NGRAM, REQUEST_DATA, RECEIVE_DATA } from './actions'

const initialState = {
  ngram: '',
  graphData: [],
}

function app(state = initialState, action) {
  switch (action.type) {
    case UPDATE_NGRAM:
      return Object.assign({}, state, {
        ngram: action.ngram
      })
    case REQUEST_DATA:
      return state
    case RECEIVE_DATA:
      return Object.assign({}, state, {
        graphData: action.data
      })
    default:
      return state
  }
}

export default app

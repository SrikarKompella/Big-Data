import request from 'request'

export const UPDATE_NGRAM = 'UPDATE_NGRAM'
export function updateNgram(ngram) {
  return { type: UPDATE_NGRAM, ngram }
}

export const REQUEST_DATA = 'REQUEST_DATA'
function requestData(ngram) {
  return { type: REQUEST_DATA, ngram }
}

export const RECEIVE_DATA = 'RECEIVE_DATA'
function receiveData(data) {
  return { type: RECEIVE_DATA, data }
}

function parseDate(graphData) {
  graphData.forEach(ngramData => {
    ngramData.data.forEach(d => {
      d.date = Date.parse(d.date)
    })
  })
}

export function fetchData(ngram) {
  return (dispatch) => {
    dispatch(requestData(ngram))

    return request
      .post({
        url: process.env.REACT_APP_API_URL + '/ngrams',
        json: true,
        body: {query: ngram}
      }, (error, response, body) => {
        if (!error && response.statusCode === 200){
          parseDate(body)
          dispatch(receiveData(body))
        }
      })
  }
}
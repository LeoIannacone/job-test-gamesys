import I from 'immutable'
import makeRequest from 'superagent-bluebird-promise'

export default url => {
  return makeRequest
  .get(`/api/${url}`)
  .then(res => {
    const body = res.body
    if (body.code !== 1) {
      return Promise.reject(body)
    }
    return I.fromJS(body.response)
  })
}

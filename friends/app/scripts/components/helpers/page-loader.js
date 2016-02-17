import React from 'react'

export default React.createClass({
  displayName: 'PageLoader',

  render() {
    return (
      <div className='pageLoader'>
        <div className='pageLoader-spin'>
          <div className='pageLoader-spin-inner'></div>
        </div>
      </div>
    )
  }
})

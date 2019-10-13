import React from 'react'
import PropTypes from 'prop-types'

const SearchComponent = ({ searchString, onChange, onClick }) => (
  <form
    onSubmit={(event) => {
      event.preventDefault()
      onClick(searchString)
    }}>
    <label>Words:</label>
    <input type='text' value={searchString} onChange={(event) => onChange(event.target.value)} />
    <input type='submit' value='Search' />
  </form>
)

SearchComponent.propTypes = {
  searchString: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onClick: PropTypes.func.isRequired,
}

export default SearchComponent

import { connect } from 'react-redux'
import { updateNgram, fetchData } from './actions'
import SearchComponent from './SearchComponent'

const mapStateToProps = state => {
  return {
    searchString: state.ngram
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onChange: ngram => {
      dispatch(updateNgram(ngram))
    },
    onClick: ngram => {
      dispatch(fetchData(ngram))
    }
  }
}

const SearchBar = connect(
  mapStateToProps,
  mapDispatchToProps
)(SearchComponent)

export default SearchBar
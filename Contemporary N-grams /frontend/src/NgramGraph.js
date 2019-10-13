import { connect } from 'react-redux'
import Graph from './Graph'

const mapStateToProps = state => {
  return {
    data: state.graphData
  }
}

const NgramGraph = connect(
  mapStateToProps
)(Graph)

export default NgramGraph
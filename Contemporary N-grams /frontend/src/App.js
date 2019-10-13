import React from 'react'
import './App.css'
import NgramGraph from './NgramGraph'
import SearchBar from './SearchBar'

const App = () => (
  <div className="App">
    <h1>Contemporary Ngrams</h1>
    <SearchBar />
    <NgramGraph/>
  </div>
)

export default App

import React, { Component } from 'react'
import PropTypes from 'prop-types'
import * as d3 from 'd3'

export default class Graph extends Component {
  static defaultProps = {
    margin: {
      top: 10,
      bottom: 50,
      left: 20,
      right: 20,
    },
    width: 800,
    height: 500,
    colors: ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3'],
  }

  static propTypes = {
    data: PropTypes.array.isRequired
  }

  componentDidMount() {
    this.drawChart()
  }

  componentDidUpdate() {
    this.removeChart()
    this.drawChart()
  }

  drawChart() {
    let svg = this.createSVG()
    let x = this.createXScale()
    let y = this.createYScale()
    let line = this.createLineGenerator(x, y)
    let g = this.createChartGroup(svg)

    this.drawXAxis(g, x)
    this.drawYAxis(g, y)
    this.drawLines(g, line)
    this.drawLegend(g)
  }

  removeChart() {
    d3
      .select('svg')
      .selectAll('*')
      .remove()
  }

  createSVG() {
    return d3
      .select('svg')
      .attr('width', this.props.width)
      .attr('height', this.props.height)
  }

  createXScale() {
    return d3
      .scaleTime()
      .range([0, this.getBodyWidth()])
      .domain(this.getXDomain())
  }

  getXDomain() {
    return this.getDataRange(d => d.date)
  }

  createYScale() {
    return d3
      .scaleLinear()
      .range([this.getBodyHeight(), this.props.margin.top])
      .domain(this.getYDomain())
  }

  getYDomain() {
    return this.getDataRange(d => d.value)
  }

  getDataRange(f) {
    let data = this.getDataArray()
    return [d3.min(data, f), d3.max(data, f)]
  }

  getDataArray() {
    return this.props.data.reduce((result, d) => result.concat(d.data), [])
  }

  createLineGenerator(xScale, yScale) {
    return d3
      .line()
      .x(d => xScale(d.date))
      .y(d => yScale(d.value))
  }

  createChartGroup(svg) {
    return svg
      .append('g')
      .attr('class', 'line-chart')
  }

  drawXAxis(group, xScale) {
    group
      .append('g')
      .attr('class', 'axis-x')
      .attr('transform', `translate(${this.props.margin.left}, ${this.getBodyHeight()})`)
      .call(d3.axisBottom(xScale))
  }

  drawYAxis(group, yScale) {
    group
      .append('g')
      .attr('class', 'axis-y')
      .attr('transform', `translate(${this.props.margin.left}, 0)`)
      .call(d3.axisLeft(yScale))
  }

  drawLines(group, lineGenerator) {
    this.props.data.forEach((d, i) => {
      group
        .append('path')
        .datum(d.data)
        .attr('d', lineGenerator)
        .attr('stroke', this.getLineColor(i))
        .attr('fill', 'none')
        .attr('transform', `translate(${this.props.margin.left}, 0)`)
    })
  }

  drawLegend(group) {
    let g = group
      .append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${this.props.margin.left + 20}, ${this.props.margin.top})`)

    this.props.data.forEach((d, i) => {
      g
        .append('rect')
        .attr('width', 10)
        .attr('height', 10)
        .attr('fill', this.getLineColor(i))
        .attr('y', i*15)

      g
        .append('text')
        .text(d.ngram)
        .attr('stroke', this.getLineColor(i))
        .attr('fill', this.getLineColor(i))
        .attr('font-size', 10)
        .attr('x', 15)
        .attr('y', i*15 + 8)
    })
  }

  getBodyHeight() {
    return this.props.height - this.props.margin.top - this.props.margin.bottom
  }

  getBodyWidth() {
    return this.props.width - this.props.margin.right - this.props.margin.left
  }

  getLineColor(i) {
    return this.props.colors[i]
  }

  render() {
    return (
      <div className="Graph">
        <svg></svg>
      </div>
    )
  }
}

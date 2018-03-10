<template lang="pug">
Card
  p(slot='title') 个股分时
  div(id='localTick' ref="localTick" :style="{width:'600px', height:'900px'}")
</template>

<script lang="coffee">
import echarts from 'echarts'
import { map } from 'ramda'
import { mapState } from 'vuex'

export default
  name: 'localTick'
  computed: mapState({
    stockTicks:(state)-> return state.stockTicks
    })

  mounted:()->
    tickChart = echarts.init document.getElementById('localTick')
    console.log @stockTicks

  watch:
    stockTicks:->
      tickChart = echarts.getInstanceByDom(@$refs.localTick)
      option =
        backgroundColor: '#fff'
        legend:
          data: ['价格']
          inactiveColor: '#777'
          textStyle: color: '#21202D'
        axisPointer:
          link: xAxisIndex: 'all'
          label: backgroundColor: '#777'
        toolbox: feature: brush: type: [
          'lineX'
          'clear'
        ]
        brush:
          xAxisIndex: 'all'
          brushLink: 'all'
          outOfBrush: colorAlpha: 0.1

        grid: [
          {
            left: '10%'
            right: '8%'
            height: '50%'
          }
          {
            left: '10%'
            right: '8%'
            top: '72%'
            height: '16%'
          }
        ]
        xAxis: [
          {
            type: 'category'
            data: @stockTicks.time
            axisLine: lineStyle: color: '#8392A5'
            axisLabel: formatter: (param) ->
              param.substr 5
            splitNumber: 500,
            min: 'dataMin',
            max: 'dataMax',
          }
          {
            type: 'category'
            gridIndex: 1
            data: @stockTicks.time
            axisLine: onZero: false
            axisTick: show: false
            splitLine: show: false
            axisLabel: show: false
            axisLine: lineStyle: color: '#8392A5'
            splitNumber: 500
            min: 'dataMin'
            max: 'dataMax'
          }
        ]
        yAxis: [
          {
            scale: true
            splitArea: show: true
            axisTick: show: false
            axisLine: lineStyle: color: '#8392A5'
          }
          {
            type: 'value'
            scale: true
            splitArea: show: true
            axisTick: show: false
            axisLine: lineStyle: color: '#8392A5'
            axisLabel: formatter: '{value} %'
          }
          {
            scale: true
            gridIndex: 1
            splitNumber: 2
            axisLabel: show: false
            axisLine: show: false
            axisTick: show: false
            splitLine: show: false
            axisLine: lineStyle: color: '#8392A5'
          }
        ]

        series: [
          {
            name: '价格'
            type: 'line'
            data: @stockTicks.values
            smooth: true
            lineStyle: normal: opacity: 0.5
            symbol: 'none'
          }
          {
            name: '成交量',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 1,
            data: @stockTicks.volumes
          }
          {
            name: '成交量',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 2,
            data: @stockTicks.volumes
          }
        ]

      tickChart.setOption option
      tickChart.on 'brushSelected', (params) =>
        pickValues = (it)=>@$store.state.stockTicks.values[it]
        @$store.dispatch 'pickStockTicks', map(pickValues,params.batch[0].selected[0].dataIndex)
</script>

<style lang='stylus'>


</style>

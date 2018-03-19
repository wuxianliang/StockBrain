<template lang="pug">
Card
  p(slot='title') 整体分时
  div(id='globalTick' ref="globalTick" :style="{width:'600px', height:'900px'}")
</template>


<script lang="coffee">
import echarts from 'echarts'
import { map, values} from 'ramda'
import { mapState } from 'vuex'

export default
  name: 'globalTick'
  computed: mapState({
    indexTicks:(state)-> return state.indexTicks
    })

  mounted:()->
    tickChart = echarts.init document.getElementById('globalTick')


  watch:
    indexTicks:->
      tickChart = echarts.getInstanceByDom(@$refs.globalTick)
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
            data: values(@indexTicks.time)
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
            data: values(@indexTicks.time)
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
            data: values(@indexTicks.prices)
            smooth: true
            lineStyle: normal: opacity: 0.5
            symbol: 'none'
          }
          {
            name: '成交量',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 1,
            data: values(@indexTicks.volumes)
          }
          {
            name: '成交量',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 2,
            data: values(@indexTicks.volumes)
          }
        ]

      tickChart.setOption option
      tickChart.on 'brushSelected', (params) =>
        pickValues = (it)=>@$store.state.indexTicks.prices[it]
        @$store.dispatch 'pickIndexTicks', map(pickValues,params.batch[0].selected[0].dataIndex)
</script>

<style lang='stylus'>


</style>

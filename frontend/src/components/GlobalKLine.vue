<template lang="pug">
  Col
    Card
      p(slot='title') 整体K线
      div(id='globalKLine' ref="globalKLine" :style="{width:'600px', height:'900px'}")
</template>

<script lang="coffee">
import echarts from 'echarts'
import {map, dropLast} from 'ramda'
import { mapState } from 'vuex'
calculateMA=(dayCount, kline)->
    result = [];
    for  i in [0...kline.prices.length]
        if i < dayCount
            result.push('-')
            continue
        sum = 0;
        for j in [ 0...dayCount]
            sum += kline.prices[i - j][1]
        result.push(+(sum / dayCount).toFixed(3))
    return result

export default
  name: 'globalKLine'
  computed: mapState({
    indexKLine:(state)-> return state.indexKLine
  })
  mounted:()->
    kLineChart = echarts.init document.getElementById('globalKLine')
    option =
      title:
        text: name
        left: 0
      animation: false
      legend:
        bottom: 10
        left: 'center'
        kline: ['日线', 'MA5', 'MA10', 'MA20', 'MA30']
      tooltip:
        trigger: 'axis'
        axisPointer:
          type: 'cross'
        backgroundColor: 'rgba(245, 245, 245, 0.8)'
        borderWidth: 1,
        borderColor: '#ccc',
        extraCssText: "width: 170px"
        padding: 10,
        textStyle:
          color: '#000'
        position: (pos, params, el, elRect, size)->
          obj = {top: 10};
          obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
          return obj
      axisPointer:
        link: {xAxisIndex: 'all'}
        label:
          backgroundColor: '#777'
      toolbox:
        feature:
          dataZoom:
            yAxisIndex: false
          brush:
            type: ['lineX', 'clear']
      brush:
        xAxisIndex: 'all',
        brushLink: 'all',
        outOfBrush:
          colorAlpha: 0.1
      visualMap:
        seriesIndex: 5,
        dimension: 2,
        pieces: [{
          value: 1,
          color: '#c23531'
        }, {
          value: -1,
          color: '#2f4554'
        }]
      grid: [
        left: '10%',
        right: '8%',
        height: '50%'
      ,
        left: '10%',
        right: '8%',
        top: '63%',
        height: '16%'
      ],
      xAxis: [
        type: 'category',
        data: @indexKLine.dates,
        scale: true,
        boundaryGap : false,
        axisLine: {onZero: false},
        splitLine: {show: false},
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax',
        axisPointer:
          z: 100
      ,
        type: 'category',
        gridIndex: 1,
        data: @indexKLine.dates,
        scale: true,
        boundaryGap : false,
        axisLine: {onZero: false},
        axisTick: {show: false},
        splitLine: {show: false},
        axisLabel: {show: false},
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax',
        axisPointer:
          label:
            formatter: (params)->
              seriesValue = (params.seriesData[0] || {}).value;
              params.value + (if seriesValue isnt null then '\n' + echarts.format.addCommas(seriesValue) else '')
      ]
      yAxis: [
        scale: true,
        splitArea:
          show: true
      ,
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: {show: false},
        axisLine: {show: false},
        axisTick: {show: false},
        splitLine: {show: false}
      ],
      dataZoom: [
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 70,
        end: 100
      ,
        show: true,
        xAxisIndex: [0, 1],
        type: 'slider',
        top: '85%',
        start: 98,
        end: 100
      ],
      series: [
          {
            name: '日线',
            type: 'candlestick',
            data: @indexKLine.prices,
            itemStyle:
              normal:
                borderColor: null,
                borderColor0: null

            tooltip:
              formatter: (param)->
                param = param[0];
                return ['Date: ' + param.name + '<hr size=1 style="margin: 3px 0">', 'Open: ' + param.data[0] + '<br/>', 'Close: ' + param.data[1] + '<br/>', 'Lowest: ' + param.data[2] + '<br/>', 'Highest: ' + param.data[3] + '<br/>'].join('')
          },
          {
            name: 'MA5',
            type: 'line',
            data: calculateMA(5, @indexKLine),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: calculateMA(10, @indexKLine),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: calculateMA(20, @indexKLine),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA30',
            type: 'line',
            data: calculateMA(30, @indexKLine),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'Volume',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: @indexKLine.volumes
          }
        ]
    kLineChart.setOption option
  watch:
    indexKLine:->
      kLineChart = echarts.getInstanceByDom(@$refs.globalKLine)
      option =
        title:
          text: name
          left: 0
        animation: false
        legend:
          bottom: 10
          left: 'center'
          kline: ['日线', 'MA5', 'MA10', 'MA20', 'MA30']
        tooltip:
          trigger: 'axis'
          axisPointer:
            type: 'cross'
          backgroundColor: 'rgba(245, 245, 245, 0.8)'
          borderWidth: 1,
          borderColor: '#ccc',
          extraCssText: "width: 170px"
          padding: 10,
          textStyle:
            color: '#000'
          position: (pos, params, el, elRect, size)->
            obj = {top: 10};
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj
        axisPointer:
          link: {xAxisIndex: 'all'}
          label:
            backgroundColor: '#777'
        toolbox:
          feature:
            dataZoom:
              yAxisIndex: false
            brush:
              type: ['lineX', 'clear']
        brush:
          xAxisIndex: 'all',
          brushLink: 'all',
          outOfBrush:
            colorAlpha: 0.1
        visualMap:
          seriesIndex: 5,
          dimension: 2,
          pieces: [{
            value: 1,
            color: '#c23531'
          }, {
            value: -1,
            color: '#2f4554'
          }]
        grid: [
          left: '10%',
          right: '8%',
          height: '50%'
        ,
          left: '10%',
          right: '8%',
          top: '63%',
          height: '16%'
        ],
        xAxis: [
          type: 'category',
          data: @indexKLine.dates,
          scale: true,
          boundaryGap : false,
          axisLine: {onZero: false},
          splitLine: {show: false},
          splitNumber: 20,
          min: 'dataMin',
          max: 'dataMax',
          axisPointer:
            z: 100
        ,
          type: 'category',
          gridIndex: 1,
          data: @indexKLine.dates,
          scale: true,
          boundaryGap : false,
          axisLine: {onZero: false},
          axisTick: {show: false},
          splitLine: {show: false},
          axisLabel: {show: false},
          splitNumber: 20,
          min: 'dataMin',
          max: 'dataMax',
          axisPointer:
            label:
              formatter: (params)->
                seriesValue = (params.seriesData[0] || {}).value;
                params.value + (if seriesValue isnt null then '\n' + echarts.format.addCommas(seriesValue) else '')
        ]
        yAxis: [
          scale: true,
          splitArea:
            show: true
        ,
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: {show: false},
          axisLine: {show: false},
          axisTick: {show: false},
          splitLine: {show: false}
        ],
        dataZoom: [
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 70,
          end: 100
        ,
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '85%',
          start: 98,
          end: 100
        ],
        series: [
            {
              name: '日线',
              type: 'candlestick',
              data: @indexKLine.prices,
              itemStyle:
                normal:
                  borderColor: null,
                  borderColor0: null

              tooltip:
                formatter: (param)->
                  param = param[0];
                  return ['Date: ' + param.name + '<hr size=1 style="margin: 3px 0">', 'Open: ' + param.data[0] + '<br/>', 'Close: ' + param.data[1] + '<br/>', 'Lowest: ' + param.data[2] + '<br/>', 'Highest: ' + param.data[3] + '<br/>'].join('')
            },
            {
              name: 'MA5',
              type: 'line',
              data: calculateMA(5, @indexKLine),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA10',
              type: 'line',
              data: calculateMA(10, @indexKLine),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA20',
              type: 'line',
              data: calculateMA(20, @indexKLine),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA30',
              type: 'line',
              data: calculateMA(30, @indexKLine),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'Volume',
              type: 'bar',
              xAxisIndex: 1,
              yAxisIndex: 1,
              data: @indexKLine.volumes
            }
          ]
      kLineChart.setOption option

      #echart 设置

      kLineChart.on 'brushSelected', (params) =>
        pickDate = (it)=>@$store.state.indexKLine.dates[it]
        pickData = (it)=>[@$store.state.indexKLine.prices[it], @$store.state.stockKLine.volumes[it]]
        @$store.dispatch 'pickIndexKRange', map(pickDate,params.batch[0].selected[0].dataIndex)
        @$store.dispatch 'pickIndexKLine', map(pickData,params.batch[0].selected[0].dataIndex)
      kLineChart.on 'click', (params) =>
        @$store.dispatch 'clickIndexKDate', {code:dropLast(3, @$store.state.indexCode), date:params.name}
        if @$store.state.stockCode isnt ''
          console.log {code:dropLast(3, @$store.state.stockCode), date:params.name}
          @$store.dispatch 'clickStockKDate', {code:@$store.state.stockCode, date:params.name}

</script>

<style lang='stylus'>


</style>

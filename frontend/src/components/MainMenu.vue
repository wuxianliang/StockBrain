<template lang="pug">
.layout-content
  Row()
    Col(name='1' span='1')
      Select(v-model='indexCodeOnPage' @on-change='changeIndex' placeholder='指数')
        Option(value='000001.SH')
         |上海
        Option(value='399001.SZ')
         |深圳
        Option(value='399006.SZ')
         |创业
    Col(name='2' span='2')
      Button(@click='showClasses = true') 板块 {{pickedStockKDate}}
      Modal(v-model='showClasses' title='板块')
        p 板块
    Col(name='3' span='2')
      DatePicker(v-model='globalDateOnPage' @on-change='changeGlobalDate' type="date" placeholder="整体日期")
    Col(name='4' span='2')
      Input(v-model='stockCodeOnPage' @on-enter='changeStockCode' placeholder="股票代码")
    Col(name='5' span='2')
      DatePicker(v-model='stockDateOnPage' @on-change='changeStockDate' type="date" placeholder="局部日期")
    Col(name='6' span='1')
    Col(name='7' span='1')
      img.logo(src='../assets/timg.jpeg' style='height:25px' )
    Col(name='9' span='2')
        DatePicker(:value='queryRangeOfTimeOnPage' type="daterange" :options='optionsOfTime' @on-change='changeQueryRangeOfTime' placeholder="查询时间区间" )
    Col(name='8' span='1')
      i-switch(v-model='frontOrBackOnPage' @on-change='changeDirection')
        span(slot='open') 前
        span(slot='close') 后
    Col(name='12' span='3')
      CheckboxGroup()
        Checkbox() 价格
        Checkbox() 成交量
        Checkbox() 板块
        Checkbox() 大盘
    Col(name='10' span='1')
      |相似度大于
    Col(name='10' span='1')
      Input(v-model='similarityOnPage' @on-change='changeSimilarity' placeholder="相似度")
    Col(name='5' span='2')
      CheckboxGroup()
        Checkbox() 同板块
        Checkbox() 同市值
        Checkbox() 同趋势
    Col(name='11' span='1')
      InputNumber(v-model='queryAmountOnPage' @on-change='changeQueryAmount' placeholder="数量")
      span 支
    Col(name='13' span='1')
      Button(@click='bigQ')
        |查询
    Col(name='14' span='2')
      i-switch(size='large')
        span(slot='open') K线
        span(slot='close') 分时
      span 优先
</template>
<script lang="coffee">
import {mapState} from 'vuex'
export default
  name: 'mainMenu'
  data: ()->
    indexCodeOnPage: ''
    globalDateOnPage: ''
    stockCodeOnPage: ''
    stockDateOnPage: ''
    frontOrBackOnPage: false
    similarityOnPage: 0.9
    queryRangeOfTimeOnPage:[]
    queryAmountOnPage: 10
    optionsOfTime:
      shortcuts:[
        {
          text: '一周',
          value:()->
            end = new Date()
            start = new Date()
            start.setTime(start.getTime()-3600*1000*24*7)
            [start, end]
        }
        {
          text: '一月',
          value:()->
            end = new Date()
            start = new Date()
            start.setTime(start.getTime()-3600*1000*24*30)
            [start, end]
        }
        {
          text: '一年',
          value:()->
            end = new Date()
            start = new Date()
            start.setTime(start.getTime()-3600*1000*24*365)
            [start, end]
        }
      ]

    showClasses: false
  computed: mapState({
    indexCode:(state)-> return state.indexCode
    queryRangeOfTime: (state)-> return state.queryRangeOfTime
    queryZone: (state)-> return state.queryZone
    globalDate: (state)-> return state.globalDate
    stockDate: (state)-> return state.stockDate
    stockCode: (state)-> return state.stockCode
    frontOrBack:(state)-> return state.frontOrBack
    similarity:(state)-> return state.similarity
    queryAmount:(state)-> return state.queryAmount
    indexKLine:(state)-> return state.indexKLine
    pickedIndexKDate:(state)-> return state.pickedIndexKDate
    pickedStockKDate:(state)-> return state.pickedStockKDate
    pickedIndexKLine:(state)-> return state.pickedIndexKLine
    pickedStockKLine:(state)-> return state.pickedStockKLine
    pickedIndexTicks:(state)-> return state.pickedIndexTicks
    pickedStockTicks:(state)-> return state.pickedStockTicks
    kLineFirst: (state)-> state.kLineFirst
  })

  methods:
    changeIndex: (indexCode)->
      @$store.dispatch('inputIndexCode', indexCode)
    changeQueryRangeOfTime:->
      @$store.dispatch('inputQueryRangeOfTime', @queryRangeOfTimeOnPage)
    changeDirection:->
      @$store.dispatch('inputDirection')
    changeGlobalDate:(value)->
      @$store.dispatch('inputGlobalDate', value)
    changeStockCode:->
      @$store.dispatch('inputStockCode', @stockCodeOnPage)
      switch @stockCodeOnPage[0]
        when '6' then @$store.dispatch('inputIndexCode', '000001.SH')
        when '0' then @$store.dispatch('inputIndexCode', '399001.SZ')
        when '3' then @$store.dispatch('inputIndexCode', '399006.SZ')
      @$store.dispatch('clearIndexTicks')
    changeStockDate:(value)->
      @$store.dispatch('inputStockDate', value)
    changeSimilarity:->
      @$store.dispatch('inputSimilarity', @similarityOnPage)
    changeQueryAmount:->
      @$store.dispatch('inputQueryAmount', @queryAmountOnPage)
    bigQ:->
      console.log @stockCode
      params =
        queryCode:@stockCode
        queryRangeOfTime: @queryRangeOfTime
        similarity: @similarity
        queryAmount: @queryAmount
        queryZone: @queryZone
        pickedStockKLine: @pickedStockKLine
        pickedStockTicks: @pickedStockTicks
        frontOrBack: @frontOrBack
        kLineFirst: @kLineFirst
      @$store.dispatch('Q', params)
</script>
<style lang="stylus">
.logo
    margin-right 1em
    margin-top 1em
    height 100%


</style>

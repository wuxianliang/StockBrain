import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import dateformat from 'dateformat'
import {reverse, split, concat, map, zip, zipWith, flatten, values} from 'ramda'
Vue.use Vuex
state =
  indexCode: ''
  indexKLine:
    prices:[]
    volumes:[]
    dates:[]
  indexTicks:{}
  #板块
  className:''
  globalDate:''
  #个股
  stockDate:''
  stockCode:''
  stockKLine:
    prices:[]
    volumes:[]
    dates:[]
  stockTicks:
    time:[]
    prices:[]
    volumes:[]
  #查询参数
  frontOrBack: false #向前或向后查询
  queryRangeOfTime:''   #查询的时间范围
  similarity: 0.9  #相似度
  queryAmount:10 #返回数量
  queryZone:''   #查询股票范围
  queryPrice:''  #价格相似
  queryVolume:'' #成交量相似
  queryClass:''  #板块走势
  queryIndex:''  #大盘走势

    #查询结果
  kResults:[]
    #交互状态
  kLineFirst: true
  pickedIndexKDate:''
  pickedIndexKLine:''
  pickedIndexKRange:''
  pickedIndexTicks:''
  #pickedClassDate:''
  #pickedClassRange:''
  pickedStockKDate:''
  pickedStockKRange:''
  pickedStockKLine:
    values:[]
    volumes:[]
  pickedStockTicks: []



#机器自己计算的数据写到getters里
getters =
  stockName: (state) ->

  #goodResult: state ->
  #实时反应的结果数据
  changesOfClasses: (state) -> #指数->涨幅热度表
  speedsOfClasses: (state) -> #指数->涨速热度表

  querySimilarKLine: (state) ->  #要查询的k线
  querySimilarTick: (state) ->   #要查询的分时图

  distributionOfChanges: (state) ->   #涨跌分布
  distributionOfSpeeds: (state) ->   #涨速分布

  currentSimilarKLine: (state) ->  #同日相似
  currentSimilarTick: (state) ->   #同时相似

  distributionOfResultKLine: (state) ->
  distributionOfResultTick: (state) ->

actions =
  #参数板
  inputIndexCode: ({commit}, indexCode)->
    path = 'http://localhost:5000/api/index_k_line'
    axios.post(path, indexCode).then((res)=>
      k=(x)->
        date: x.TRADE_DT#.toString("utf8"),#.slice(0, 4)+"-"+x.TRADE_DT.toString("utf8").slice(4, 6)+"-"+x.TRADE_DT.toString("utf8").slice(6, 9),
        volume: x.S_DQ_VOLUME,
        value: [x.S_DQ_OPEN, x.S_DQ_CLOSE, x.S_DQ_LOW, x.S_DQ_HIGH]
      date = (it)->it.date
      dates = map(date, map(k, values(res.data)))
      value = (it)->it.value
      prices= map(value, map(k, values(res.data)))
      upDown = (it)-> if it.value[0]>it.value[1] then -1 else 1
      volume = (it)->it.volume
      volumes= map(flatten, zip([0...dates.length], zip(map(volume, map(k, values(res.data))), map(upDown, map(k, values(res.data))))))
      commit 'CHANGE_INDEX_KLINE', {dates, prices, volumes}
      commit('CHANGE_INDEX', indexCode))

  inputGlobalDate: ({commit}, globalDate)-> commit('CHANGE_GLOBAL_DATE', globalDate)
  inputClassName: ->
  inputStockCode: ({commit}, stockCode)->
    path = 'http://localhost:5000/api/stock_k_line'
    axios.post(path, stockCode).then((res)=>
      console.log res.data
      k=(x)->
        date: x.TRADE_DT#.toString("utf8"),#.slice(0, 4)+"-"+x.TRADE_DT.toString("utf8").slice(4, 6)+"-"+x.TRADE_DT.toString("utf8").slice(6, 9),
        volume: x.S_DQ_VOLUME,
        value: [x.S_DQ_OPEN, x.S_DQ_CLOSE, x.S_DQ_LOW, x.S_DQ_HIGH]
      date = (it)->it.date
      dates = map(date, map(k, values(res.data)))
      value = (it)->it.value
      prices= map(value, map(k, values(res.data)))
      upDown = (it)-> if it.value[0]>it.value[1] then -1 else 1
      volume = (it)->it.volume
      volumes= map(flatten, zip([0...dates.length], zip(map(volume, map(k, values(res.data))), map(upDown, map(k, values(res.data))))))
      commit 'CHANGE_STOCK_KLINE', {dates, prices, volumes}
      commit('CHANGE_STOCK_CODE', stockCode))
  inputStockDate: ({commit}, stockDate)-> commit('CHANGE_STOCK_DATE', stockDate)
  inputQueryRangeOfTime: ({commit}, value)-> commit('CHANGE_QUERY_RANGE_OF_TIME', value)
  inputDirection:({commit})-> commit('CHANGE_DIRECTION')
  inputSimilarity: ({commit}, similarity)-> commit('CHANGE_SIMILARITY', similarity)
  inputQueryAmount:({commit}, queryAmount)-> commit('CHANGE_QUERYAMOUNT', queryAmount)
  #整体k线
  clickIndexKDate: ({commit}, data)->
    path = 'http://localhost:5000/api/index_ticks'
    axios.post(path, data).then((res)=>
      commit 'CHANGE_INDEX_TICKS', res.data
      commit 'CHANGE_INDEX_K_DATE', data.date)
  clearIndexTicks:({commit})->
    commit 'CHANGE_INDEX_TICKS', {time:[], prices:[],volumes:[]}
  pickInexKRange: ({commit}, value)-> commit('CHANGE_INDEX_K_RANGE', value)
  pickIndexKLine: ({commit}, value)->
    commit('CHANGE_INDEX_K_LINE', value)
  clickStockKDate: ({commit}, data)->
    path = 'http://localhost:5000/api/stock_ticks'
    axios.post(path, data).then((res)=>
      console.log res.data
      commit 'CHANGE_STOCK_TICKS', map(reverse, map(values, res.data))
      commit('CHANGE_STOCK_K_DATE', data.date))
  pickStockKRange: ({commit}, value)->
    commit('CHANGE_PICKED_STOCK_K_RANGE', value)
  pickStockKLine: ({commit}, value)->
    commit('CHANGE_PICKED_STOCK_K_LINE', value)
  changeKLineOfClass: ->
  changeHeadOfDragen: ->
  clickClassDate: ->
  pickClassRange: ->
  clickTickDate: ->
  pickIndexTicks: ({commit}, value) ->
    normalize = (it)-> it/value[0]
    commit('CHANGE_PICKED_INDEX_TICKS', map(normalize, value))
  pickStockTicks: ({commit}, value) ->
    normalize = (it)-> it/value[0]
    commit('CHANGE_PICKED_STOCK_TICKS', map(normalize, value))
  lookHeadOfDragen: -> #当日板块龙头股
  Q:({commit}, params)->
    path = 'http://localhost:5000/api/similar_k_line'
    axios.post(path, params).then((res)=>

      results = values(res.data)
      #results = values(values(res.data)[0])
      kResults = []
      for stock in results
        stock = values(JSON.parse(stock))
        k=(x)->
          code: x.S_INFO_WINDCODE #not yet
          date: dateformat(x.TRADE_DT, 'isoDate')#.toString("utf8"),#.slice(0, 4)+"-"+x.TRADE_DT.toString("utf8").slice(4, 6)+"-"+x.TRADE_DT.toString("utf8").slice(6, 9),
          volume: x.S_DQ_VOLUME,
          value: [x.S_DQ_OPEN, x.S_DQ_CLOSE, x.S_DQ_LOW, x.S_DQ_HIGH]
        date = (it)->it.date
        dates = map(date, map(k, stock))

        code = map(((it)->it.code), map(k, stock))[0]

        value = (it)->it.value
        prices= map(value, map(k, stock))

        upDown = (it)-> if it.value[0]>it.value[1] then -1 else 1
        volume = (it)->it.volume
        volumes= map(flatten, zip([0...dates.length], zip(map(volume, map(k, stock)), map(upDown, map(k, stock)))))
        kResults.push({code, dates, prices, volumes})
      console.log kResults
      commit('CHANGE_RESULTS', kResults))


mutations =
  CHANGE_INDEX:(state, indexCode)-> state.indexCode = indexCode
  CHANGE_QUERY_RANGE_OF_TIME: (state, value) -> state.queryRangeOfTime = value
  CHANGE_DIRECTION:(state)-> state.frontOrBack = !state.frontOrBack
  CHANGE_STOCK_CODE:(state, value)-> state.stockCode = value
  CHANGE_GLOBAL_DATE:(state, value)-> state.globalDate = value
  CHANGE_SIMILARITY:(state, value)-> state.similarity = value
  CHANGE_QUERYAMOUNT:(state, value)-> state.queryAmount = value
  CHANGE_INDEX_KLINE:(state, value)-> state.indexKLine = value
  CHANGE_STOCK_KLINE:(state, value)-> state.stockKLine = value
  CHANGE_PICKED_INDEX_K_RANGE:(state, value)-> state.pickedIndexKRange = value
  CHANGE_PICKED_INDEX_K_LINE:(state, value)-> state.pickedIndexKLine = value
  CHANGE_INDEX_K_DATE:(state, value)-> state.pickedIndexKDate = value
  CHANGE_INDEX_TICKS:(state, value)-> state.indexTicks = value
  CHANGE_STOCK_K_DATE:(state, value)-> state.pickedStockKDate = value
  CHANGE_PICKED_STOCK_K_RANGE:(state, value)->state.pickedStockKRange = value
  CHANGE_PICKED_STOCK_K_LINE:(state, value)->state.pickedStockKLine = value
  CHANGE_STOCK_TICKS:(state, value)-> state.stockTicks = value
  CHANGE_PICKED_STOCK_TICKS:(state, value)->state.pickedStockTicks = value
  CHANGE_PICKED_INDEX_TICKS:(state, value)->state.pickedIndexTicks = value
  CHANGE_RESULTS:(state, value)-> state.kResults = value
export default new Vuex.Store(
  state: state
  getters: getters
  actions: actions
  mutations: mutations

)

<template lang="pug">
    .layout-content
      Row
        Col(span='6')
          globalKLine()
          localKLine()
        Col(span='6')
          globalTick()
          localTick()
        Col(span='6')
          resultKLineChart
        Col(span='6')
          resultTickChart

</template>
<script lang="coffee">
import zerorpc from "zerorpc"
import globalKLine from './GlobalKLine'
import localKLine from './LocalKLine'
import globalTick from './GlobalTick'
import localTick from './LocalTick'
import resultKLineChart from './ResultKLineChart'
import resultTickChart from './ResultTickChart'


export default
  name: 'mainContainer'
  components: { globalKLine, localKLine, globalTick, localTick, resultKLineChart, resultTickChart }
  data: ->
    result: '@$store.state.stockNumber'
  computed:
    kdata:-> @$store.state.kLine.kdata
    name: -> @$store.state.kLine.name
    code: -> @$store.state.kLine.code
    similars: -> @$store.state.kLine.similars
  methods:
    open: (link) -> @$electron.shell.openExternal link


</script>
<style lang="stylus">


</style>

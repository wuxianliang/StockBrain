<template lang="pug">
  div
    Home
</template>

<script lang="coffee">
import Home from '@/components/Home'

export default
    name: 'app'
    components: { Home }
</script>

<style lang="stylus">
#app
    font-family Arial, sans-serif
    text-align: center
    color #2c3e50
    margin-top 60px
a
    display inline-block
    padding 1em
</style>

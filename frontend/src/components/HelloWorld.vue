<template lang="pug">
div.hello
  h1 Hello
  h1 Count: {{ state.count }} {{ randomNumber }}
  button(@click="incrCount") Increment
</template>

<script lang="coffee">
import store from './Store'
import axios from 'axios'
export default
    name: 'HelloWorld'
    data: () ->
        state: store.state
        randomNumber:0
    methods:
        incrCount: ->
            path = "http://localhost:5000/api/random"
            axios.get path
            .then (response)=> @randomNumber = response.data.randomNumber
            .catch (error)=>console.log error
            store.commit 'increment'
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
h1, h2
  font-weight normal
</style>

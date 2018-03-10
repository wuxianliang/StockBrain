<template lang="pug">
  .layout
    mainMenu
    mainContainer
</template>

<script lang="coffee">
  import mainMenu from './MainMenu'
  import mainContainer from './MainContainer'
  export default
    name: 'Home'
    components: { mainContainer, mainMenu }

</script>

<style lang='stylus'>


</style>

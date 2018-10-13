<template>
  <div id="app">
    <router-view></router-view>
    <notifications group="foo" />
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

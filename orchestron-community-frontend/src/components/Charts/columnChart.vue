<template>
  <div>
    <br>
    <p class="title">{{ chartTitle }}</p>
    <hr>
    <column-chart :data="chartData"></column-chart>
  </div>
</template>

<script>
  export default {
    name: 'appColumnChart',
    props: {
      chartData: {
        type: Array,
        required: true
      },
      chartTitle: {
        type: String,
        required: true
      }
    }
  }
</script>

<style scoped>
  .title {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }
</style>

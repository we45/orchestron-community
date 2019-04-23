<template>
  <div>
    <br>
    <p class="title">{{ barChartTitle }}</p>
    <hr>
    <bar-chart :data="barChartData"></bar-chart>
  </div>
</template>

<script>
  export default {
    name: 'AppBarChart',
    props: {
      barChartData: {
        type: Array,
        required: true
      },
      barChartTitle: {
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

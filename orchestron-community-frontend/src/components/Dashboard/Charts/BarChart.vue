<template>
  <div>
    <br>
    <p>{{ barChartTitle }}</p>
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

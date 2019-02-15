<template>
<div>
  <b-container fluid style="background-color: #FFFFFF">
  <br>
  <p class="title" v-if="title">{{ title }}</p>
  <hr>
  <vue-highcharts :options="options"></vue-highcharts>
  </b-container>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
  export default {
    name: 'orchyStackedBarChart',
    components: {
      VueHighcharts
    },
    props: {
      chartData: {
        type: Array,
        required: false
      },
      title: {
        type: String,
        required: false
      },
      chartCategories: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        options: {
          chart: {
            type: 'bar'
          },
          title: {
            text: ''
          },
          xAxis: {
            categories: this.chartCategories
          },
          yAxis: {
            min: 0,
            title: {
              text: 'Count'
            }
          },
          legend: {
            reversed: true
          },
          plotOptions: {
            series: {
              stacking: 'normal'
            }
          },
          series: this.chartData
        }
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
  font-weight: 200;
  }
</style>

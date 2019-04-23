<template>
<div>
  <br>
  <p class="title" v-if="title">{{ title }}</p>
  <hr>
  <b-badge variant="danger" style="float: right;" v-if="chartSubTitle"> From - {{ chartSubTitle }}</b-badge>
  <br>
  <vue-highcharts :options="options"></vue-highcharts>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
    export default {
        name: 'orchyReportStackedBarChart',
      components: {
          VueHighcharts
      },
      props:{
        title: {
            type: String,
            required: false
          },
        chartSubTitle: {
            type: String,
            required: false
          },
        options: {
           required: false
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

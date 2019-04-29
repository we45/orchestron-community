<template>
<div>
  <br>
    <p class="title">{{ title }}</p>
    <hr>
    <template  v-if="cweData">
      
  <vue-highcharts :options="options"></vue-highcharts>
    </template>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
    export default {
        name: 'OrchyBasicBarChart',
      components: {
          VueHighcharts
      },
      props:{
          cweData: {
            type: Array,
            required: true
          },
          cweDataRange:{
              type: Array,
              required: true
          },
          title: {
            type: String,
            required: false
          },
      },
      data() {
          return {
            options: {
              chart: {
              type: 'column',
              styledMode: true,
              options3d: {
              enabled: true,
              alpha: 15,
              beta: 15,
              depth: 50
    }
  },
  title: {
    text: ''
  },
  plotOptions: {
    column: {
      depth: 25
    }
  },
  yAxis:{
    name: 'helo'
  },
  xAxis: {
    categories: this.cweDataRange,
    // label: 'CWES'
  },
  series: [{
    data: this.cweData,
    colorByPoint: true,
    showInLegend: false,
    name: 'Count',
  }]

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
  }
</style>

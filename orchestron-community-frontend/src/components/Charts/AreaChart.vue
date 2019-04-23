<template>
<div>
  <br>
  <p class="title">{{ title }}</p>
  <hr>
  <br>
  <vue-highcharts :options="options"></vue-highcharts>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
    export default {
        name: 'OrchyAreaChart',
      components: {
          VueHighcharts
      },
      props:{
          areaChartData: {
            type: Array,
            required: true
          },
        title: {
            type: String,
            required: true
          }
      },
      data() {
          return {
            options: {
          chart: {
            type: 'area'
          },
          title: {
            text: ''
          },
          xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
          },
          yAxis: {
            title: {
              text: 'Count'
            },
            labels: {
            formatter: function () {
                return this.value;
                }
            }
          },
          tooltip: {
            // crosshairs: true,
            // shared: true
            split: true,
            valueSuffix: 'Vulnerabilities'
          },
          credits: {
            enabled: false
          },
          plotOptions: {
            spline: {
              marker: {
                radius: 4,
                lineColor: '#666666',
                lineWidth: 1
              }
            }
          },
          series: this.areaChartData
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

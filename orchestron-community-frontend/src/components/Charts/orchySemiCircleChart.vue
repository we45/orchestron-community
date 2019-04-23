<template>
<div>
      <vue-highcharts :options="options"></vue-highcharts>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
    export default {
        name: 'orchySemiCircleChart',
      components: {
          VueHighcharts
      },
      props:{
          areaChartData: {
            type: Array,
            required: false
          },
        title: {
            type: String,
            required: false
          }
      },
      data() {
          return {
            options: {
          chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
          },
          title: {
            text: 'Vulnerability Stats'
          },
          tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Vulnerabilities',
        innerSize: '50%',
        data: this.areaChartData,
      colors: ['#d11d55', '#ff9c2c', '#008b8f', '#1d1e52']
    }]
        }
          }
      }
    }
</script>

<style scoped>

</style>

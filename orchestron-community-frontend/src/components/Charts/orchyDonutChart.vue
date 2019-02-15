<template>
<div>
  <b-container fluid style="background-color: #FFFFFF">
    <br>
    <p class="title">{{ orchy_donutTitle }}</p>
    <hr>
      <vue-highcharts :options="options"></vue-highcharts>

  </b-container>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
    export default {
        name: 'orchyDonutChart',
      components: {
          VueHighcharts
      },
      props:{
          areaChartData: {
            type: Array,
            required: false
          },
        orchy_donutTitle: {
            type: String,
            required: false
          },
        tooltipLabel: {
            type: String,
          required: false
        }
      },
      data() {
          return {
            // orchy_donutTitle: "Vulnerability by severity",
            options: {
          chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
          },
          title: {
            text: ''
          },
          tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: false,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
          showInLegend: true,
            startAngle: 180,
            endAngle: 180,
            center: ['50%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: this.tooltipLabel,
        innerSize: '50%',
        data: this.areaChartData

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
  font-weight: 200;
  }
</style>

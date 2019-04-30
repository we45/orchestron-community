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
    name: 'orchyPieChart',
    components: {
      VueHighcharts
    },
    props: {
      title: {
        type: String,
        required: false
      },
      chartData: {
        type: Array,
        required: true
      },
      tooltipLabel: {
        type: String,
        required: false
      }
    },
    data() {
      return {
        options: {
          chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
          },
          title: {
            text: ' '
          },
          tooltip: {
            pointFormat: '{series.name}: <b>{point.y}</b>'
          },
          plotOptions: {
            pie: {
              allowPointSelect: true,
              cursor: 'pointer',
              dataLabels: {
                enabled: false
              },
              showInLegend: true
            }
          },
          series: [{
            name: this.tooltipLabel,
            colorByPoint: true,
            data: this.chartData

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

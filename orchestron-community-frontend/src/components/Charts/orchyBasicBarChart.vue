<template>
<div>
  <br>
    <p class="title">{{ title }}</p>
    <hr>
  <vue-highcharts :options="options"></vue-highcharts>
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
          basicBarChartData: {
            type: Array,
            required: true
          },
        title: {
            type: String,
            required: true
          },
        barChartCategory: {
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
            text: ' '
          },
          xAxis: {
              categories: this.barChartCategory,
              title: {
                  text: null
              }
          },
          yAxis: {
            min: 0,
            title: {
                text: 'Counts',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' Vulnerability'
        },
          plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
              legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 80,
        floating: true,
        borderWidth: 1,
        // backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        shadow: true
    },
    credits: {
        enabled: false
    },
          series: this.basicBarChartData
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

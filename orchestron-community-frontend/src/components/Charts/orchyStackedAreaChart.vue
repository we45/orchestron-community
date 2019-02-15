<template>
  <div>
    <b-container fluid style="background-color: #FFFFFF">
      <br>
      <p class="title">{{ title }}</p>
      <hr>
      <vue-highcharts :options="options"></vue-highcharts>
      </b-container>
</div>

</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
  export default {
    name: 'orchyStackedAreaChart',
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
        required: false
      },
      chartCategories: {
        type: Array,
        required: false
      }
    },
    data() {
      return {
        // title: 'Vulnerabilities by severity',
        options: {
          chart: {
            type: 'area'
          },
          title: {
            text: ''
          },
          subtitle: {
            text: ''
          },
          xAxis: {
            categories: this.chartCategories,
            tickmarkPlacement: 'on',
            title: {
              enabled: false
            }
          },
          yAxis: {
            title: {
              text: 'Vulnerabilities Count'
            },
            labels: {
              formatter: function() {
                return this.value / 1000
              }
            }
          },
          tooltip: {
            split: true,
            valueSuffix: 'vulnerabilities'
          },
          plotOptions: {
            area: {
              stacking: 'normal',
              lineColor: '#666666',
              lineWidth: 1,
              marker: {
                lineWidth: 1,
                lineColor: '#666666'
              }
            }
          },
          series: this.chartData,
          colors: ['#d11d55', '#ff9c2c', '#008b8f', '#1d1e52']

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

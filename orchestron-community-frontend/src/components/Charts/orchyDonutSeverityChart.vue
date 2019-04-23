<template>
<div>
  <b-container fluid style="background-color: #FFFFFF">
    <br>
  <p class="title">Vulnerabilities by severity</p>
  <hr>
  <b-row style="background-color: #FFFFFF;">
    <b-col cols="9">
      <template v-if="chartData.length > 0">
      <vue-highcharts :options="options"></vue-highcharts>
        </template>
      <template v-else>
        No Data
      </template>
    </b-col>
    <b-col cols="3">
      <br>
      <br>
                <b-col cols="3" v-if="highCount > 0">
                    <router-link  :to="{ path: 'severity_wise/high/' }" >
                        <div class="high-round">
                            <span>{{ highCount }}</span>
                        </div>
                    </router-link>
                </b-col>
                 <b-col cols="3" v-else>
                        <div class="high-round">
                            <span>{{ highCount }}</span>
                        </div>
                </b-col>
                <br>
                <b-col cols="3" v-if="mediumCount >0 ">
                    <router-link  :to="{ path: 'severity_wise/medium/'}" >
                        <div class="medium-round">
                            <span>{{ mediumCount }}</span>
                        </div>
                    </router-link>
                </b-col>
                 <b-col cols="3" v-else>
                    <div class="medium-round">
                        <span>{{ mediumCount }}</span>
                    </div>
                </b-col>
                <br>
                <b-col cols="3" v-if="lowCount >0 ">
                    <router-link  :to="{ path: 'severity_wise/low/'}" >
                        <div class="low-round">
                            <span>{{ lowCount }}</span>
                        </div>
                    </router-link>
                </b-col>
                <b-col cols="3" v-else>
                    <div class="low-round">
                        <span>{{ lowCount }}</span>
                    </div>
                </b-col>
                <br>
                <b-col cols="3" v-if="infoCount > 0">
                    <router-link  :to="{ path: 'severity_wise/info/'}" >
                        <div class="info-round">
                            <span>{{ infoCount }}</span>
                        </div>
                    </router-link>
                </b-col>
                <b-col cols="3" v-else>
                        <div class="info-round">
                            <span>{{ infoCount }}</span>
                        </div>
                </b-col>
            </b-col>
  </b-row>
    </b-container>
</div>
</template>

<script>
  import VueHighcharts from 'vue2-highcharts'
  export default {
    name: 'orchyDonutSeverityChart',
    components: {
      VueHighcharts
    },
    props: {
      chartData: {
        type: Array
      },
      highCount: {
        type: Number
      },
      mediumCount: {
        type: Number
      },
      lowCount: {
        type: Number
      },
      infoCount: {
        type: Number
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
            text: ' '
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
            name: 'Severity',
            innerSize: '50%',
            data: this.chartData,
            colors: ['#d11d55', '#ff9c2c', '#008b8f', '#1d1e52']

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
  .high-round {
    display: inline-block;
    height: 40px;
    width: 40px;
    line-height: 40px;
    -moz-border-radius: 20px;
    border-radius: 20px;
    background-color: #d11d55;
    color: #FFFFFF;
    text-align: center;
  }

  .medium-round {
    display: inline-block;
    height: 40px;
    width: 40px;
    line-height: 40px;
    -moz-border-radius: 20px;
    border-radius: 20px;
    background-color: #ff9c2c;
    color: #FFFFFF;
    text-align: center;
  }

  .low-round {
    display: inline-block;
    height: 40px;
    width: 40px;
    line-height: 40px;
    -moz-border-radius: 20px;
    border-radius: 20px;
    background-color: #008b8f;
    color: #FFFFFF;
    text-align: center;
  }

  .info-round {
    display: inline-block;
    height: 40px;
    width: 40px;
    line-height: 40px;
    -moz-border-radius: 20px;
    border-radius: 20px;
    background-color: #1d1e52;
    color: #FFFFFF;
    text-align: center;
  }
</style>

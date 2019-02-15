<template>
    <div>
      <b-container fluid style="background-color: #FFFFFF">
        <br/>
        <p class="title">{{ title }}</p>
        <hr>
        <b-row>
            <b-col cols="9">
                <pie-chart :data=" chartData "
                           :donut="true" :colors="['#d11d55', '#ff9c2c', '#008b8f', '#1d1e52']" legend="bottom"></pie-chart>
            </b-col>
            <b-col cols="3">
               <b-col cols="3" >
                      <div class="high-round">
                          <span>{{ highCount }}</span>
                      </div>
              </b-col>
                <br>
                 <b-col cols="3" >
                    <div class="medium-round">
                        <span>{{ mediumCount }}</span>
                    </div>
                </b-col>
                <br>
                <b-col cols="3">
                    <div class="low-round">
                        <span>{{ lowCount }}</span>
                    </div>
                </b-col>
                <br>
                <b-col cols="3">
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

export default {
  name: 'reportDonutChart',
  props: {
    title: {
      type: String
    },
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
  }
}
</script>

<style scoped>

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
.title {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
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

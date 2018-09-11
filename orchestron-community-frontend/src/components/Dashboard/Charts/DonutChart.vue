<template>
    <div>
        <br/>
        <p>{{ title }}</p>
        <hr>
        <b-row>
            <b-col cols="9">
                <pie-chart :data=" chartData "
                           :donut="true" :colors="['#d11d55', '#ff9c2c', '#008b8f', '#1d1e52']" legend="bottom"></pie-chart>
            </b-col>
            <b-col cols="3">
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
    </div>
</template>

<script>

export default {
  name: 'DonutChart',
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

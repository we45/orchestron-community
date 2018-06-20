<template>
    <div>
     <b-progress class="mt-1" style="height:10px;width: 100%;" v-if="total">
        <b-progress-bar :value="(high*100)/total" class="high-progress-bar" v-b-tooltip.hover :title=" 'High - ' + high"></b-progress-bar>
        <b-progress-bar :value="(medium*100)/total" class="medium-progress-bar" v-b-tooltip.hover :title=" 'Medium - ' + medium"></b-progress-bar>
        <b-progress-bar :value="(low*100)/total" class="low-progress-bar" v-b-tooltip.hover :title=" 'Low - ' + low"></b-progress-bar>
        <b-progress-bar :value="(info*100)/total" class="info-progress-bar" v-b-tooltip.hover :title=" 'Info - ' + info"></b-progress-bar>
      </b-progress>
    </div>
</template>

<script>
    export default {
      name: 'VulProgressBar',
      props: {
        high: {
          required: true
        },
        medium: {
          required: true
        },
        low: {
          required: true
        },
        info: {
          required: true
        },
        total: {
          required: true
        }
      }
    }
</script>

<style scoped>
  .high-progress-bar {
    float: left;
    width: 0;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #FFFFFF;
    text-align: center;
    background-color: #d11d55;
    -webkit-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    -webkit-transition: width .6s ease;
    -o-transition: width .6s ease;
    transition: width .6s ease;
  }

  .medium-progress-bar {
    float: left;
    width: 0;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #FFFFFF;
    text-align: center;
    background-color: #ff9c2c;
    -webkit-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    -webkit-transition: width .6s ease;
    -o-transition: width .6s ease;
    transition: width .6s ease;
  }

  .low-progress-bar {
    float: left;
    width: 0;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #FFFFFF;
    text-align: center;
    background-color: #008b8f;
    -webkit-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    -webkit-transition: width .6s ease;
    -o-transition: width .6s ease;
    transition: width .6s ease;
  }

  .info-progress-bar {
    float: left;
    width: 0;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #FFFFFF;
    text-align: center;
    background-color: #1d1e52;
    -webkit-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .15);
    -webkit-transition: width .6s ease;
    -o-transition: width .6s ease;
    transition: width .6s ease;
  }
</style>

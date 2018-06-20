<template>
    <div>
        <br>
        <b-container fluid>
            <b-row>
                <b-col cols="8">
                    <p>Vulnerabilities - {{ subTitle }}</p>
                </b-col>
                <b-col cols="4">
                    <p class="m3_left panel_label_info"><span class="high_badge"></span>High</p>
                    <p class="m3_left panel_label_info"><span class="medium_badge"></span> Medium</p>
                    <p class="m3_left panel_label_info"><span class="low_badge"></span> Low</p>
                    <p class="m3_left panel_label_info"><span class="info_badge"></span> Info</p>
                </b-col>
            </b-row>
            <hr>
            <b-row v-for="vul in limitBy(vulData,5) " :key="vul.name">
                <b-col cols="4">
                    <router-link  :to="{ path: nameUrl + vul.id }" >
                        <p class="title">{{ vul.name }}</p>
                    </router-link>
                </b-col>
                <b-col cols="6">
                    <b-progress class="mt-1">
                        <b-progress-bar :value="(vul.high*100)/vul.total" class="high-progress-bar"
                            v-b-tooltip.hover :title=" 'High - '+vul.high  " ></b-progress-bar>
                        <b-progress-bar :value="(vul.medium*100)/vul.total" class="medium-progress-bar" v-b-tooltip.hover :title=" 'Medium - '+vul.medium  "></b-progress-bar>
                        <b-progress-bar :value="(vul.low*100)/vul.total" class="low-progress-bar" v-b-tooltip.hover :title=" 'Low - '+vul.low  "></b-progress-bar>
                        <b-progress-bar :value="(vul.info*100)/vul.total" class="info-progress-bar" v-b-tooltip.hover :title=" 'Info - '+vul.info  "></b-progress-bar>
                    </b-progress>
                </b-col>
                <b-col cols="2">
                    <p> <strong class="vul-count"> {{ vul.total }} </strong> <span class="vul-desc"> Vulnerabilities </span></p>
                </b-col>
                <br>
                <br>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
      name: 'VulProgressBarStats',
      props: {
        vulData: {
          type: Array,
          required: true
        },
        subTitle: {
          type: String,
          required: true
        },
        nameUrl: {
          type: String,
          required: false
        }
      }
    }
</script>

<style scoped>
  .m3_left {
    margin-left: 3%;
  }

  .title {
    color: #000000;
    font-family: 'Avenir';
    font-size: 14px;
  }

  .vul-count {
    font-family: 'Avenir';
    font-size: 30px;
    font-weight: 300;
    line-height: 0.53;
    color: #232328;
  }

  .vul-desc {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.5;
    color: #979797;
    padding-left: 5%;
  }

  .high_badge {
    display: inline-block;
    min-width: 15px;
    padding: 3px 7px;
    font-size: 12px;
    line-height: 1;
    color: #FFFFFF;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    background-color: #d11d55;
    border-radius: 15px;
    height: 15px;
    margin-right: 3%;
  }

  .medium_badge {
    display: inline-block;
    min-width: 15px;
    padding: 3px 7px;
    font-size: 12px;
    line-height: 1;
    color: #FFFFFF;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    background-color: #ff9c2c;
    border-radius: 15px;
    height: 15px;
    margin-right: 3%;
  }

  .low_badge {
    display: inline-block;
    min-width: 15px;
    padding: 3px 7px;
    font-size: 12px;
    line-height: 1;
    color: #FFFFFF;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    background-color: #008b8f;
    border-radius: 15px;
    height: 15px;
    margin-right: 3%;
  }

  .info_badge {
    display: inline-block;
    min-width: 15px;
    padding: 3px 7px;
    font-size: 12px;
    line-height: 1;
    color: #FFFFFF;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    background-color: #1d1e52;
    border-radius: 15px;
    height: 15px;
    margin-right: 3%;
  }

  .panel_label_info {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 2.64;
    color: #6b7784;
    display: inline;
  }

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

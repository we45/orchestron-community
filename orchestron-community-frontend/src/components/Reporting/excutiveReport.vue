<template>
  <div>
    <b-container fluid>
      <b-row v-if="excutivedata.open_vuls.length > 0">
        <b-col cols="4">
            <center>
              <br/>
              <p class="title">Open Vulnerabilities</p>
              <br>
              <p>
                  
                  <strong class="open-vul-count">
                 {{excutivedata.open_vul_count}}
                  </strong>
              </p>
            </center>
        </b-col>
        <b-col cols="4">
              <center>
                  <br/>
                  <p class="title">Closed Vulnerabilities</p>
                  <br>
                      <p>
                          <strong class="closed-vul-count">
                          {{  excutivedata.closed_vul_count }}
                          </strong>
                      </p>
              </center>
        </b-col>
        <b-col cols="4">
            <center>
                <br/>
                <p class="title">False Positive</p>
                <br>
                <p class="org-grade-no-data">{{  excutivedata.false_positive_count }}</p>
            </center>
        </b-col>
      </b-row>
    </b-container>
    <br>
    <hr>
    <br>
    <b-row>
      <b-col cols="6" v-if="excutiveSeverityChartData.length > 0" xs="6">
        <report-donut-chart
            :chartData="excutiveSeverityChartData"
            :title="'Severity Chart'"
            :highCount="excutiveHighCount"
            :mediumCount="excutiveMediumCount"
            :lowCount="excutiveLowCount"
            :infoCount="excutiveInfoCount"></report-donut-chart>
      </b-col>
      <b-col cols="6" xs="6" v-if="excutiveVulAgeingCategories.length>0">
        <orchy-report-stacked-bar-chart :options="excutiveVulAgeingOptions"
                                        :title="'Vulnerabilities Ageing'"
                                        :chartSubTitle="excutiveVulAgeingSubTitle"></orchy-report-stacked-bar-chart>
      </b-col>
    </b-row>
    <br>
    <hr>
    <br>
    <template v-if="excutiveVulDataItems.length > 0">
      <excutive-vul-info :excutiveVulDataItems="excutiveVulDataItems"
                         :excutiveNoPages="excutiveNoPages"
                         @clickPagination="paginationClick($event)"></excutive-vul-info>
    </template>
    <br>
    <br>
    
    
    <template v-if="excutiveOwaspchartData.length > 0">
      <orchy-report-stacked-bar-chart :options="excutiveowaspOptions" :title="'OWASP Stats'"></orchy-report-stacked-bar-chart>
    </template>

    <!--  <template v-if="excutiveOwaspchartData.length > 0">
      <orchy-report-stacked-bar-chart :options="excutiveowaspOptions" :title="'OWASP Stats'"></orchy-report-stacked-bar-chart>
    </template> -->
    <br>
  </div>
</template>

<script>
  // import AppBarChart from '@/components/Charts/BarChart'
  // import appColumnChart from '@/components/Charts/columnChart'
  import reportDonutChart from '@/components/Charts/reportDonutChart'
  // import impactTable from '@/components/Reporting/impactTable'
  import excutiveVulInfo from '@/components/Reporting/excutiveVulInfo'
  // import OrchyAreaChart from '@/components/Charts/AreaChart'
  import orchyReportStackedBarChart from '@/components/Charts/orchyReportStackedBarChart'


  export default {
    name: 'excutiveReport',
    components: {
      // AppBarChart,
      // appColumnChart,
      reportDonutChart,
      // impactTable,
      excutiveVulInfo,
      // OrchyAreaChart,
      orchyReportStackedBarChart
    },
    props: {
      excutivedata: {
        // type: Array,
        required: true
      },
      excutiveSeverityChartData: {
        type: Array,
        required: true
      },
      excutiveReOpenVulData: {
        type: Array,
        required: true
      },
      excutiveVulImpactData: {
        type: Array,
        required: true
      },
      excutiveVulDataItems: {
        type: Array,
        required: true
      },
      excutiveVulAgeingCategories: {
        type: Array,
        required: true
      },
      excutiveVulAgeingSubTitle: {
        required: false
      },
      excutiveHighCount: {
        // type: Array,
        required: false
      },
      excutiveMediumCount: {
        // type: Array,
        required: false
      },
      excutiveLowCount: {
        // type: Array,
        required: false
      },
      excutiveInfoCount: {
        // type: Array,
        required: false
      },
      excutiveNoPages: {
        // type: Array,
        required: false
      },
      excutiveOwaspCategory: {
        type: Array,
        required: false
      },
      excutiveOwaspchartData: {
        type: Array,
        required: false
      },
      excutiveVulAgeingData: {
        type: Array,
        required: false
      },
      excutiveVulAgeingOptions: {
        // type: Array,
        required: false
      },
      excutiveowaspOptions: {
        // type: Array,
        required: false
      }

    },
    data() {
      return {
        items: [],
        vulAgeingData: [],
        vulAgeingCategories: [],
        columnChartData: [['Injection', 32], ['BrokenAccessControl', 46], ['UnCategorised', 28]],
        dataItems: [],
        highCount: 0,
        mediumCount: 0,
        lowCount: 0,
        infoCount: 0,
        severityChartData: [],
        vulImpactData: [],
        vulRisk: [],
        reOpenVulData: [],
        reportHeadingData: [],
        isOrlUpdated: false,
        currentPage: 1,
        areaChartData: [{
                name: 'High',
                data: [502, 635, 809, 947, 1402, 3634, 5268],
                color: '#d11d55'
            }, {
                name: 'Medium',
                data: [106, 107, 111, 133, 221, 767, 1766],
                color: '#ff9c2c'
            }, {
                name: 'Low',
                data: [163, 203, 276, 408, 547, 729, 628],
                color: '#008b8f'
            }, {
                name: 'Info',
                data: [18, 31, 54, 156, 339, 818, 1201],
                color: '#1d1e52'
            }],

        areaChartTitle: 'Monthly Vulnerability Stats',
        stackedChartTitle: 'OWASP Vulnerability Stats',
        stackedChartData: [{
        name: 'High',
        data: [5, 3, 4, 7],
          color: '#d11d55'
    }, {
        name: 'Medium',
        data: [2, 2, 3, 2],
          color: '#ff9c2c'
    }, {
        name: 'Low',
        data: [3, 4, 4, 2],
          color: '#008b8f'
    }, {
        name: 'Info',
        data: [0, 1, 9, 8],
          color: '#1d1e52'
    }]

      }
    },
    methods: {
      paginationClick(event) {
        this.$emit('clickPagination', { page: event.page })
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

.high {
  background-color: #d11d55;
  color: #EEEEEE;
  font-size: 20px;
  font-family: Avenir;
}
.medium {
  background-color: #ff9c2c;
  color: #EEEEEE;
  font-size: 20px;
  font-family: Avenir;
}
.low {
  background-color: #008b8f;
  color: #EEEEEE;
  font-size: 20px;
  font-family: Avenir;
}
.info {
  background-color: #1d1e52;
  color: #EEEEEE;
  font-size: 20px;
  font-family: Avenir;
}
.high-badge {
  background-color: #d11d55;
  color: #EEEEEE;
  font-size: 12px;
  font-family: Avenir;
}
.medium-badge {
  background-color: #ff9c2c;
  color: #EEEEEE;
  font-size: 12px;
  font-family: Avenir;
}
.low-badge {
  background-color: #008b8f;
  color: #EEEEEE;
  font-size: 12px;
  font-family: Avenir;
}
.info-badge {
  background-color: #1d1e52;
  color: #EEEEEE;
  font-size: 12px;
  font-family: Avenir;
}
.info-box {
  display: block;
  min-height: 70px;
  background: #FF4C4C;
  width: 100%;
  border-radius: 8px;
  /*border-top-left-radius: 8px;*/
}
.info-box-icon {
  border-bottom-left-radius: 8px;
  border-top-left-radius: 8px;
  display: block;
  float: left;
  height: 70px;
  width: 120px;
  text-align: center;
  font-family: 'Avenir';
  font-size: 16px;
  line-height: 1.55;
  background: #FF4C4C;
  color: #EEEEEE;
  padding-top: 3%;
  margin-right: 20px;
}

.info-box-content {
  padding: 20px 5px;
  margin-left: 90px;
  border-right: #FF4C4C 1px solid;
  border-top: #FF4C4C 1px solid;
  border-bottom: #FF4C4C 1px solid;
  height: 70px;
  width: 90px;
  border-bottom-right-radius: 8px;
  border-top-right-radius: 8px;
  background-color: #FF4C4C;

}
.info-box-number {
  display: block;
  font-weight: bold;
  font-family: 'Avenir';
  font-size: 18px;
  color: #EEEEEE;
}

.close-box {
  display: block;
  min-height: 70px;
  background: #00AB69;
  width: 100%;
  border-radius: 8px;
  /*border-top-left-radius: 8px;*/
}
.close-box-icon {
  border-bottom-left-radius: 8px;
  border-top-left-radius: 8px;
  display: block;
  float: left;
  height: 70px;
  width: 120px;
  text-align: center;
  font-family: 'Avenir';
  font-size: 16px;
  line-height: 1.55;
  background: #00AB69;
  color: #EEEEEE;
  padding-top: 3%;
  margin-right: 20px;
}

.close-box-content {
  padding: 20px 5px;
  margin-left: 90px;
  border-right: #00AB69 1px solid;
  border-top: #00AB69 1px solid;
  border-bottom: #00AB69 1px solid;
  height: 70px;
  width: 90px;
  border-bottom-right-radius: 8px;
  border-top-right-radius: 8px;
  background-color: #00AB69;

}
.close-box-number {
  display: block;
  font-weight: bold;
  font-family: 'Avenir';
  font-size: 18px;
  color: #EEEEEE;
}

.avg-box {
  display: block;
  min-height: 70px;
  background: #d11d55;
  width: 100%;
  border-radius: 8px;
  /*border-top-left-radius: 8px;*/
}
.avg-box-icon {
  border-bottom-left-radius: 8px;
  border-top-left-radius: 8px;
  display: block;
  float: left;
  height: 70px;
  width: 80px;
  text-align: center;
  font-family: 'Avenir';
  font-size: 16px;
  line-height: 1.55;
  background: #d11d55;
  color: #EEEEEE;
  padding-top: 3%;
  margin-right: 20px;
}

.avg-box-content {
  padding: 20px 5px;
  margin-left: 90px;
  border-right: #d11d55 1px solid;
  border-top: #d11d55 1px solid;
  border-bottom: #d11d55 1px solid;
  height: 70px;
  width: 150px;
  border-bottom-right-radius: 8px;
  border-top-right-radius: 8px;
  background-color: #d11d55;

}
.avg-box-number {
 /* padding: 20px 5px;
  display: block;
  font-weight: bold;
  font-family: 'Avenir';
  font-size: 18px;
  color: #EEEEEE;*/


  display: block;
  font-weight: bold;
  font-family: 'Avenir';
  font-size: 18px;
  color: #EEEEEE;
}




  .title {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }

  .open-vul-count {
    font-family: 'Avenir';
    color: #FF4C4C;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .closed-vul-count {
    font-family: 'Avenir';
    color: #00AB69;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .org-grade-no-data {
    font-family: 'Avenir';
    color: #d11d55;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }


</style>

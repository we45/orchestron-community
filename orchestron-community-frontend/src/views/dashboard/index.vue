<template>
  <div>
    <b-container fluid>
      <loading :active.sync="isLoading" :can-cancel="true"></loading>
      <!-- <b-row>
        <b-col>
          <vul-count-section
                :openVul="openVulCount"
                :closedVul="closedVulCount"
                :grade="grade"
                :openVulUrl=" '/org/openvuls' "
                :closedVulUrl=" '/org/closed_vul' "></vul-count-section>
        </b-col>
      </b-row> -->

      <b-row>
        <b-col id="vul_count_section">
          <header-count-section
            :openVul="openVulCount"
                :closedVul="closedVulCount"
                :grade="grade"
                :openVulUrl="openVulUrl"
                :closedVulUrl="closedVulUrl"
            :unCategorised="unCategorisedCount"
            :uncategorized_vul="uncategorized_vul"
          ></header-count-section>
        </b-col>
      </b-row>
      <!-- <br> -->
      <br>
      <b-row>
        <b-col cols="4">
            <template v-if="severityChartData.length > 0">
              <orchy-donut-severity-chart
                :chartData="severityChartData"
                :highCount="high"
                :mediumCount="medium"
                :lowCount="low"
                :infoCount="info"
              >
              </orchy-donut-severity-chart>
            </template>
        </b-col>
        <b-col cols="4">
          <template v-if="toolVulnerabilityChart.length > 0">
            <orchy-pie-chart :title="toolVulChartTitle" :chartData="toolVulnerabilityChart" :tooltipLabel="'tool'"></orchy-pie-chart>
          </template>
        </b-col>
        <b-col cols="4">
            <template v-if="appVulnerabilityChart.length > 0">
              <orchy-pie-chart :title="appVulChartTitle" :chartData="appVulnerabilityChart" :tooltipLabel="'application'"></orchy-pie-chart>
            </template>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-col cols="6">
            <template v-if="basicBarDashboardChartData.length > 0">
                <orchy-stacked-bar-chart :chartData="basicBarDashboardChartData"
                                        :chartCategories="dashboardCategories"
                                        :title="'Vulnerabilities Aging Analysis'"></orchy-stacked-bar-chart>
            </template>
        </b-col>
        <b-col cols="6">
           <template v-if="taxanomyData.length > 0">
              <orchy-donut-chart
            :orchy_donutTitle="taxonomyChartTitle" :areaChartData="taxanomyData" :tooltipLabel="'OWASP'"></orchy-donut-chart>
              </template>
        </b-col>
        
      </b-row>
      <br>
      <b-row>
        <b-col cols="12">

        </b-col>
      </b-row>
      <!-- <b-row>
        <b-col cols="12">
          <template v-if="toolVulnerabilityChart.length > 0">
            <orchy-pie-chart :title="toolVulChartTitle" :chartData="toolVulnerabilityChart" :tooltipLabel="'tool'"></orchy-pie-chart>
          </template>
        </b-col>
      </b-row> -->
       <!-- <b-container fluid>
      <b-row style="background-color: #FFFFFF;">
        <b-col cols="6">
          <donut-chart
            :chartData="severityChartData"
            :title="title"
            :highCount="high"
            :mediumCount="medium"
            :lowCount="low"
            :infoCount="info"></donut-chart>
        </b-col>
        <b-col cols="6">
            <app-bar-chart :barChartData="vulAgeingData" :barChartTitle="'Vulnerabilities Ageing - Applications'"></app-bar-chart>
        </b-col>
      </b-row>
       </b-container> -->
        <br>
        <!-- <b-tabs style="background-color: #FFFFFF;">
          <b-tab title="Applications" small>
            <div>
              <vul-progress-bar-stats
                :vulData="appData"
                :subTitle=" 'Applications' "
                :nameUrl="'/projects/individual_application/'"></vul-progress-bar-stats>
            </div>
          </b-tab>
          <b-tab title="Scan Tools" small>
            <div>
              <vul-progress-bar-stats :vulData="scanToolData" :subTitle=" 'Scan Tools' " :nameUrl="'individual_tool/'"></vul-progress-bar-stats>
            </div>
          </b-tab>
        </b-tabs> -->
      <br>
      <br>
    </b-container>
  </div>
</template>

<script>
import DonutChart from '@/components/Dashboard/Charts/DonutChart'
import AppBarChart from '@/components/Dashboard/Charts/BarChart'
import VulProgressBarStats from '@/components/Dashboard/VulProgressBarStats'
import VulCountSection from '@/components/Dashboard/VulCountSection'
import axios from '@/utils/auth'
import { notValidUser } from '@/utils/checkAuthUser'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.min.css'
import headerCountSection from '@/components/Dashboard/headerCountSection'
import orchyDonutSeverityChart from '@/components/Charts/orchyDonutSeverityChart'
import orchyPieChart from '@/components/Charts/orchyPieChart'
import orchyStackedBarChart from '@/components/Charts/orchyStackedBarChart'
import orchyDonutChart from '@/components/Charts/orchyDonutChart'

export default {
  name: 'dashboard',
  components: {
    DonutChart,
    AppBarChart,
    VulProgressBarStats,
    VulCountSection,
    Loading,
    headerCountSection,
    orchyDonutSeverityChart,
    orchyPieChart,
    orchyStackedBarChart,
    orchyDonutChart
  },
  data() {
    return {
      openVulCount: 0,
      closedVulCount: 0,
      openVulUrl: '/org/openvuls',
      closedVulUrl: '/org/closed_vul',
      title: 'Severity-Wise',
      appBarCharttitle: 'Vulnerabilities Ageing',
      high: 0,
      medium: 0,
      low: 0,
      info: 0,
      severityChartData: [],
      vulAgeingData: [],
      appData: [],
      scanToolData: [],
      owaspData: [],
      heatmapData: [],
      grade: '',
      appSevData: [],
      isLoading: false,
      openVulUrl: '/org/openvuls/',
      closedVulUrl: '/org/closed_vul/',
      uncategorized_vul: '/org/uncategorized_vul/',
      unCategorisedCount: 0,
      appVulnerabilityChart: [],
      appVulChartTitle: 'Vulnerabilities by application',
      dashboardCategories: [],
      basicBarDashboardChartData: [],
      taxonomyChartTitle: 'Vulnerability by taxanomy',
      taxanomyData: [],
      toolVulnerabilityChart: [],
      toolVulChartTitle: 'Vulnerabilities by tool',
    }
  },
  created() {
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
    this.fetchData()
  },
  methods: {
    fetchData() {
      if (this.org && this.token) {
        axios.get('/organizations/' + this.org + '/?apps=1&tool=1&ageing=1&severity=1&&opened=1&closed=1&avg_ageing=1&owasp=1')
          .then(res => {
            this.isLoading = true
            this.closedVulCount = res.data.closed_vul_count
            this.openVulCount = res.data.open_vul_count
            this.high = res.data.severity[3] | 0
            this.medium = res.data.severity[2] | 0
            this.low = res.data.severity[1] | 0
            this.info = res.data.severity[0] | 0
            this.scanToolData = []
            this.owaspData = []
            this.severityChartData = []
            this.appData = []
            this.grade = res.data.avg_ageing

            this.severityChartData.push(
              ['High', this.high],
              ['Medium', this.medium],
              ['Low', this.low],
              ['Info', this.info]
            )
            this.appVulnerabilityChart = []
            
            for (const [key, val] of Object.entries(res.data.applications)) {
              this.appData.push({
                name: key,
                high: val.sev[3],
                medium: val.sev[2],
                low: val.sev[1],
                info: val.sev[0],
                total: val.sev[3] + val.sev[2] + val.sev[1] + val.sev[0],
                id: val.id
              })
              this.appSevData.push([key, (val.sev[3] + val.sev[2] + val.sev[1] + val.sev[0])])

              this.appVulnerabilityChart.push({
                  name: key,
                  y: val.sev[3] + val.sev[2] + val.sev[1] + val.sev[0]
                })
            }
            // this.appData = this.appData.orderBy(this.appData, ['total'], ['desc'])
            // for (const [key, val] of Object.entries(res.data.tools)) {
            //   this.scanToolData.push({
            //     name: key,
            //     high: val[3],
            //     medium: val[2],
            //     low: val[1],
            //     info: val[0],
            //     total: val[3] + val[2] + val[1] + val[0],
            //     id: btoa(unescape(encodeURIComponent(key)))
            //   })
            // }
            // for (const ageing of res.data.ageing) {
            //   this.vulAgeingData.push(ageing)
            // }
            console.log("owasp data", res.data.owasp)
            for (const [key, val] of Object.entries(res.data.owasp)) {
                // this.owaspData.push({
                //   name: key,
                //   high: val[3],
                //   medium: val[2],
                //   low: val[1],
                //   info: val[0],
                //   total: val[3] + val[2] + val[1] + val[0],
                //   id: btoa(unescape(encodeURIComponent(key))),
                //   sevUrl: '/org/individual_owasp/' + btoa(unescape(encodeURIComponent(key))) + '/severity_wise/'
                // })

                this.taxanomyData.push({
                  name: key,
                  y: val[3] + val[2] + val[1] + val[0]
                })
              }

              for (const [key, val] of Object.entries(res.data.tools)) {
                // this.scanToolData.push({
                //   name: key,
                //   high: val[3],
                //   medium: val[2],
                //   low: val[1],
                //   info: val[0],
                //   total: val[3] + val[2] + val[1] + val[0],
                //   id: btoa(unescape(encodeURIComponent(key))),
                //   sevUrl: '/org/individual_tool/' + btoa(unescape(encodeURIComponent(key))) + '/severity_wise/'
                // })
                this.toolVulnerabilityChart.push({
                  name: key,
                  y: val[3] + val[2] + val[1] + val[0]
                })
              }
              



            const highAgeingSevCount = []
            const mediumAgeingSevCount = []
            const lowAgeingSevCount = []
            const infoAgeingSevCount = []
            for (const [key, value] of Object.entries(res.data.ageing)) {
                for (const [keys, values] of Object.entries(value)) {
                this.dashboardCategories.push(keys)
                  highAgeingSevCount.push(values[3])
                  mediumAgeingSevCount.push(values[2])
                  lowAgeingSevCount.push(values[1])
                  infoAgeingSevCount.push(values[0])
              }
              }
              this.basicBarDashboardChartData.push(
                {
                  name: this.highLable,
                  data: highAgeingSevCount,
                  color: '#d11d55'
                }
              )

              this.basicBarDashboardChartData.push(
                {
                  name: this.mediumLable,
                  data: mediumAgeingSevCount,
                  color: '#ff9c2c'
                }
              )

              this.basicBarDashboardChartData.push(
                {
                  name: this.lowLable,
                  data: lowAgeingSevCount,
                  color: '#008b8f'
                }
              )

              this.basicBarDashboardChartData.push(
                {
                  name: this.infoLable,
                  data: infoAgeingSevCount,
                  color: '#1d1e52'
                }
              )
            this.isLoading = false
          }).catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
      } else {
        notValidUser()
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>

</style>

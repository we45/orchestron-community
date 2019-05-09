<template>
    <div>
        <b-container fluid>
            <loading :active.sync="reloadPage" :can-cancel="true"></loading>
            <engagement-header :engagementHeader="engagementHeader"></engagement-header>
            <br>
            <b-container fluid>
                <b-row style="background-color: #FFFFFF;">
                    <b-col cols="6">
                        <donut-chart
                            :chartData="chartData"
                            :title="title"
                            :highCount="highCount"
                            :mediumCount="mediumCount"
                            :lowCount="lowCount"
                            :infoCount="infoCount"></donut-chart>
                    </b-col>
                    <b-col cols="6">
                        <!-- <app-bar-chart :barChartData="vulAgeingData" :barChartTitle="'Scans-wise Stats'"></app-bar-chart> -->
                                <orchy-stacked-bar-chart v-if="ageingChart.length > 0 && ageingCategory.length > 0" :chartData="ageingChart"
                                        :chartCategories="ageingCategory"
                                        :title="'Vulnerabilities by ageing analysis'"></orchy-stacked-bar-chart>
                    </b-col>
                </b-row>
            </b-container>
            <br>
            <b-container fluid style="background-color: #FFFFFF;">
                <br>
                <p class="title">Assign Scans</p>
                <hr>
                <p style="text-align: right;margin-right: 3%;"> <span class="count-text">There are </span> <span class="count-circle">{{ scanCount }}</span>
                    <span class="count-text">Unassigned scans for</span> <span>{{ appName }}</span>  <span class="count-text"> application</span>
                </p>
                <form>
                    <v-select
                        v-model="assignedScans"
                        placeholder="Select scans"
                        :options='scanListOptions'
                        multiple>
                    </v-select>
                    <br>
                    <b-button class="pull-right btn btn-orange"
                        v-on:click="submitAssignedScans"
                        style="float: right; margin-right: 3%;"
                        v-if="assignedScans">Assign</b-button>
                </form>
                <br>
                <br>
            </b-container>
            <br>
            <b-container fluid style="background-color: #FFFFFF;">
              <br>
              <p class="title">List of Scans</p>
                <hr>
                <scans
                    :dataItems="vulnerabilitiesList"
                    @deleteModal="deleteModal($event)"></scans>
            </b-container>
        </b-container>
    </div>
</template>

<script>
    import EngagementHeader from '../../components/Engagements/Header'
    // import DonutChart from '@/components/Dashboard/Charts/DonutChart'

    import DonutChart from '@/components/Charts/orchyDonutSeverityChart'
    import AppBarChart from '@/components/Dashboard/Charts/BarChart'
    import Scans from '../../components/Application/Scans'
    import axios from '@/utils/auth'
    import Loading from 'vue-loading-overlay'
    import 'vue-loading-overlay/dist/vue-loading.min.css'
    import { notValidUser } from '@/utils/checkAuthUser'
    import engAgeing from '@/components/Charts/orchyStackedBarChart'
    import orchyStackedBarChart from '@/components/Charts/orchyStackedBarChart'


    export default {
      name: 'individualEngagement',
      components: {
        EngagementHeader,
        DonutChart,
        AppBarChart,
        Scans,
        Loading,
        engAgeing,
        orchyStackedBarChart
      },
      data() {
        return {
          isLoading: false,
          reloadPage: false,
          vulnerabilitiesList: [],
          engagementHeader: [],
          applicationLists: [],
          appName: '',
          scanCount: 0,
          chartData: [],
          title: 'Engagement Severity',
          highCount: 0,
          mediumCount: 0,
          lowCount: 0,
          infoCount: 0,
          scanListOptions: [],
          assignedScans: [],
          appId: '',
          vulAgeingData: [],
          ageingChart: [] ,
          ageingCategory: [],
          highLable: 'High',
          mediumLable: 'Medium',
          lowLable: 'Low',
          infoLable: 'Info',
        }
      },
      created() {
        this.org = localStorage.getItem('org')
        this.token = localStorage.getItem('token')
        this.param = this.$route.params.engagementId
        this.fetchData()
      },
      methods: {
        fetchData() {
          if (this.org && this.token) {
            this.reloadPage = true
            axios.get('/engagements/' + this.param + '/?scans=1')
              .then(res => {
                this.appId = res.data.app_details.id
                this.appName = res.data.app_details.name
                this.infoCount = res.data.severity[0] | 0
                this.lowCount = res.data.severity[1] | 0
                this.mediumCount = res.data.severity[2] | 0
                this.highCount = res.data.severity[3] | 0
                this.chartData.push(
                  ['High', this.highCount],
                  ['Medium', this.mediumCount],
                  ['Low', this.lowCount],
                  ['Info', this.infoCount]
                )
                this.engagementHeader.push({
                  'name': res.data.name,
                  'appName': this.appName,
                  'desc': res.data.description,
                  'closedBy': res.data.closed_by,
                  'startDate': res.data.start_date,
                  'stopDate': res.data.stop_date,
                  'closedDate': res.data.closed_on
                })

             

                 this.ageingCategory = []
              this.ageingChart = []
                var highAgeingSevCount = []
                var mediumAgeingSevCount = []
                var lowAgeingSevCount = []
                var infoAgeingSevCount = []
                for (const [key, value] of Object.entries(res.data.ageing['ageing'])) {
                  for (const [keys, values] of Object.entries(value)) {
                  this.ageingCategory.push(keys)
                    highAgeingSevCount.push(values[3])
                    mediumAgeingSevCount.push(values[2])
                    lowAgeingSevCount.push(values[1])
                    infoAgeingSevCount.push(values[0])
                }
                }
                this.ageingChart.push(
                  {
                    name: this.highLable,
                    data: highAgeingSevCount,
                    color: '#d11d55'
                  }
                )

                this.ageingChart.push(
                  {
                    name: this.mediumLable,
                    data: mediumAgeingSevCount,
                    color: '#ff9c2c'
                  }
                )

                this.ageingChart.push(
                  {
                    name: this.lowLable,
                    data: lowAgeingSevCount,
                    color: '#008b8f'
                  }
                )

                this.ageingChart.push(
                  {
                    name: this.infoLable,
                    data: infoAgeingSevCount,
                    color: '#1d1e52'
                  }
                )




                for (const value of res.data.scans) {
                  this.vulnerabilitiesList.push({
                    name: value.fields.short_name,
                    sev: value.stats.severity_count,
                    id: value.fields.id,
                    scanDate: value.fields.created_on,
                    scanType: value.fields.scan_type,
                    triggeredBy: value.fields.triggered_by,
                    tool: value.fields.tool,
                    scanId: value.fields.id,
                    url: '/projects/individual_application/' + this.appId + '/individual_scan/' + value.fields.id + '/',
                    appDashboard: false
                  })
                  const vulTotal = (value.stats.severity_count[3] + value.stats.severity_count[2] + value.stats.severity_count[1] + value.stats.severity_count[0])
                  this.vulAgeingData.push([value.fields.scan_type,vulTotal])
                }
                axios.get('/applications/' + res.data.application + '/?scans=1&unassigned=1')
                  .then(res => {
                    for (const value of res.data.scans) {
                      this.scanListOptions.push({ value: value.fields.name, label: value.fields.short_name })
                    }
                    this.scanCount = this.scanListOptions.length
                  }).catch(error => {
                   this.reloadPage = false

                    if (error.res.status === 404) {
                      this.$router.push('/not_found')
                    } else if (error.res.status === 403) {
                      this.$router.push('/forbidden')
                    } else {
                      this.$router.push('/error')
                    }
                  })


            this.reloadPage = false


              }).catch(error => {
            this.reloadPage = false

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
        },
        submitAssignedScans() {
          if (this.org && this.token) {
            this.reloadPage = true

            const assignedScans = []
            for (const val of this.assignedScans) {
              assignedScans.push(val.value)
            }
            const form_data = {
              scans: assignedScans
            }
            axios.post('/engagements/' + this.param + '/scans/assign/', form_data)
              .then(res => {
                this.isLoading = true
                this.$router.go('/engagements/individual_engagement/' + this.param + '/')
                this.$notify({
                  group: 'foo',
                  type: 'success',
                  title: 'success',
                  text: 'The scans has been included successfully!',
                  position: 'top right'
                })
                this.isLoading = false
            this.reloadPage = false

              }).catch(error => {
            this.reloadPage = false
                
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
.title{
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }
  .count-circle {
      background: #F44336;
      border-radius: 2em;
      -moz-border-radius: 2em;
      -webkit-border-radius: 2em;
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
      display: inline-block;
      line-height: 2em;
      margin-right: 5px;
      text-align: center;
      width: 2em;
      font-family: 'Avenir';
  }
  .count-text{
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }
.btn-orange {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:focus,
  .btn-orange.focus {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }
</style>

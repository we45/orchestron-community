<template>
    <div>
        <b-container fluid>
          <loading :active.sync="isLoading" :can-cancel="true"></loading>
          <app-headers
                :name="appname"
                :logo="appLogo"
                :url="appUrl"
                :osInfo="appOsInfo"
                :platform="appPlatform" @configureApplication="applicationConfigure()"></app-headers>

          <b-container v-if="showConfig" fluid style="background-color: #FFFFFF;">
            <br>
               <b-row class="my-1">
                  <b-col sm="2"><label class="label">JIRA Project:</label></b-col>
                  <b-col sm="10">
                    <v-select v-model="appJiraProject" :options="appJiraProjectOptions" placeholder="Select JIRA Project"></v-select>
                  </b-col>
              </b-row>
              <br>
            <button type="button"
                    class="btn btn-orange-close pull-right"
                    @click=" submitAppJiraConfig() " style="float: right;">
                Submit
                </button>
            <br>
            <br>
            <br>
          </b-container>
            <br>
            <vul-count-section
                :openVul="openVulCount"
                :closedVul="closeVulCount"
                :grade="appGrade"
                :openVulUrl=" '/projects/individual_application/open_vul/'+ appId  "
                :closedVulUrl=" '/projects/individual_application/closed_vul/' + appId  "></vul-count-section>
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
                        <app-bar-chart :barChartData="appSevData" :barChartTitle="'Application-wise Vulnerabilities'"></app-bar-chart>
                    </b-col>
                </b-row>
            </b-container>
            <br>
            <!--Scans-->
            <b-tabs style="background-color: #FFFFFF;">
                <b-tab title="Scans" small>
                    <div>
                        <br>
                        <b-container fluid>
                            <scans
                                :dataItems="vulnerabilitiesList"
                                @deleteModal="deleteModal($event)"></scans>
                        </b-container>
                    </div>
                </b-tab>
                <b-tab title="Upload Results" small @click="uploadResultsClick">
                    <div>
                        <b-container fluid style="background-color: #FFFFFF;">
                            <br>
                            <br>
                            <form @submit.prevent="submitUploadResult">
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Tool:</label></b-col>
                                    <b-col sm="10">
                                        <v-select :options="toolOption"
                                            placeholder="Select Tool"
                                            v-model="uploadTool"
                                            :state="!$v.uploadTool.$invalid"></v-select>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Name:</label></b-col>
                                    <b-col sm="10">
                                        <b-form-input
                                            v-model="uploadName"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter Name" :state="!$v.uploadName.$invalid"></b-form-input>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Upload File:</label></b-col>
                                    <b-col sm="10">
                                        <b-form-file
                                            v-model="uploadFile"
                                            placeholder="Choose a file..."
                                            accept="xml,json"
                                            :state="!$v.uploadFile.$invalid"></b-form-file>
                                        <br>
                                        <p>{{ uploadFile.name }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                            </form>
                            <b-col col="12" >
                                <div class="pull-right" style="float: right">
                                    <button type="button"
                                        class="btn btn-orange-close pull-right"
                                        @click=" submitUploadResult() " v-if="!$v.uploadTool.$invalid && !$v.uploadName.$invalid && !$v.uploadFile.$invalid">
                                    Submit
                                    </button>
                                </div>
                            </b-col>
                            <br>
                            <br>
                        </b-container>
                    </div>
                </b-tab>
                <b-tab title="Manual Entry" small @click="createManualScan">
                    <div>
                        <b-container fluid style="background-color: #FFFFFF;">
                            <br>
                            <br>
                            <form v-if="manualStepOne">
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Scan Name:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-input
                                            v-model="manualScanName"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter Scan Name" :state="!$v.manualScanName.$invalid"></b-form-input>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Vulnerability Name:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-input
                                            v-model="manualVulName"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter Vulnerability Name" :state="!$v.manualVulName.$invalid"></b-form-input>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">CWE:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-input
                                            v-model="manualCwe"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter CWE" :state="!$v.manualCwe.$invalid"></b-form-input>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Severity:</label></b-col>
                                    <b-col sm="10">
                                      <v-select
                                        :options="manualSeverityList"
                                        v-model="manualSeverity"
                                        placeholder="Select Severity" :state="!$v.manualSeverity.$invalid"></v-select>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">OWASP:</label></b-col>
                                    <b-col sm="10">
                                      <v-select
                                        :options="manualOwaspList"
                                        v-model="manualOwasp"
                                        placeholder="Select OWASP" :state="!$v.manualOwasp.$invalid"></v-select>
                                    </b-col>
                                </b-row>
                                <br>
                                <br>
                              <b-col col="12" >
                                <div class="pull-right" style="float: right">
                                    <button type="button"
                                        class="btn btn-orange-close pull-right"
                                        @click=" createManualScanStepOne() " v-if="!$v.manualScanName.$invalid && !$v.manualVulName.$invalid
                                        && !$v.manualCwe.$invalid && !$v.manualSeverity.$invalid && !$v.manualOwasp.$invalid">
                                    Next
                                    </button>
                                </div>
                            </b-col>
                            </form>
                            <form v-if="manualStepTwo">
                              <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Description:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulDesc"
                                            type="text"
                                            class="inline-form-control"
                                            :rows="3"
                                            :max-rows="6"
                                            placeholder="Enter Description" :state="!$v.manualVulDesc.$invalid"></b-form-textarea>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Remediation:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulRemedy"
                                            type="text"
                                            class="inline-form-control"
                                            :rows="3"
                                            :max-rows="6"
                                            placeholder="Enter Description" :state="!$v.manualVulRemedy.$invalid"></b-form-textarea>
                                    </b-col>
                                </b-row>
                                <br>
                                <br>
                               <button type="button"
                                        class="btn btn-orange-close pull-left"
                                        @click="prevManualScanStepOne() ">
                                    Previous
                                    </button>
                              <button type="button"
                                      style="float: right;"
                                        class="btn btn-orange-close pull-right"
                                        @click="createManualScanStepTwo() " v-if="!$v.manualVulDesc.$invalid && !$v.manualVulRemedy.$invalid">
                                    Next
                                    </button>
                              <br>
                            </form>
                            <br>
                            <form v-if="manualStepThree">
                              <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">URL:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulUrl"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter URL" :state="!$v.manualVulUrl.$invalid"></b-form-textarea>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Parameter:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulParam"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter Parameter" :state="!$v.manualVulParam.$invalid"></b-form-textarea>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Description:</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulUrlDesc"
                                            type="text"
                                            class="inline-form-control"
                                            :rows="3"
                                            :max-rows="6"
                                            placeholder="Enter URL Description" :state="!$v.manualVulUrlDesc.$invalid"></b-form-textarea>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">File:</label></b-col>
                                    <b-col sm="10">
                                        <b-form-file
                                            v-model="manualVulUrlFile"
                                            placeholder="Choose a File..."
                                            :state="!$v.manualVulUrlFile.$invalid"></b-form-file>
                                        <br>
                                        <p>{{ manualVulUrlFile.name }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                                <br>
                              <button type="button"
                                        class="btn btn-orange-close pull-left"
                                        @click="prevManualScanStepTwo() ">
                                    Previous
                                    </button>
                              <button type="button"
                                      style="float: right;"
                                        class="btn btn-orange-close pull-right"
                                        @click="createManualScanWithVul() " v-if="!$v.manualVulUrl.$invalid && !$v.manualVulParam.$invalid && !$v.manualVulUrlDesc.$invalid && !$v.manualVulUrlFile.$invalid">
                                    Submit
                                    </button>
                            </form>
                            <br>
                        </b-container>
                    </div>
                </b-tab>
            </b-tabs>
            <!--Delete Modal-->
            <b-modal ref="deleteScanModal" hide-footer title="Delete Scan" centered>
                <div>
                    <form @submit.prevent="submitDeleteScan">
                        <input type="hidden" v-model="deleteScanId">
                        <h5>Are you sure want to delete this scan ?</h5>
                        <br>
                        <hr>
                        <div class="pull-right">
                            <button type="button" class="btn btn-orange-submit" data-dismiss="modal" @click=" submitDeleteScan() " style="float: right">
                            Delete
                            </button>
                            <button type="button" class="btn btn-orange-close" @click=" closeDeleteScan()" style="float: right">Cancel</button>
                        </div>
                    </form>
                </div>
            </b-modal>
        </b-container>
    </div>
</template>

<script>
  import AppHeaders from '../../components/Application/Headers'
  import Scans from '../../components/Application/Scans'
  import VulCountSection from '@/components/Dashboard/VulCountSection'
  import DonutChart from '@/components/Dashboard/Charts/DonutChart'
  import AppBarChart from '@/components/Dashboard/Charts/BarChart'
  import axios from '@/utils/auth'
  import { required, minLength, url } from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import { notValidUser } from '@/utils/checkAuthUser'

  export default {
    name: 'IndividualApplication',
    components: {
      AppHeaders,
      Scans,
      VulCountSection,
      DonutChart,
      AppBarChart,
      Loading
    },
    data() {
      return {
        isLoading: false,
        vulnerabilitiesList: [],
        appname: '',
        appId: '',
        appLogo: '',
        appUrl: '',
        appOsInfo: '',
        appPlatform: '',
        deleteScanId: '',
        chartData: [],
        title: 'Severity Status',
        highCount: 0,
        mediumCount: 0,
        lowCount: 0,
        infoCount: 0,
        openVulCount: 0,
        closeVulCount: 0,
        appGrade: 0,
        uploadName: '',
        uploadFile: '',
        toolOption: [],
        uploadTool: '',
        manualScanName: '',
        manualVulName: '',
        manualCwe: '',
        manualSeverityList: [
          { label: 'High', value: 3 },
          { label: 'Medium', value: 2 },
          { label: 'Low', value: 1 },
          { label: 'Info', value: 0 }
        ],
        manualSeverity: 0,
        manualOwaspList: ['Injection', 'Broken Authentication', 'Sensitive Data Exposure', 'XML External Entities (XXE)',
          'Broken Access Control', 'Security Misconfiguration', 'Cross-Site Scripting (XSS)', 'Insecure Deserialization',
          'Using Components with Known Vulnerabilities', 'Insufficient Logging&Monitoring', 'Uncategorized'],
        manualOwasp: '',
        manualStepOne: false,
        manualStepTwo: false,
        manualVulDesc: '',
        manualVulRemedy: '',
        manualStepThree: false,
        manualVulUrl: '',
        manualVulParam: '',
        manualVulUrlDesc: '',
        manualVulUrlFile: '',
        manualScanId: '',
        manualScanVulId: '',
        appSevData: [],
        parsingStatus: '',
        parsingScanId: '',
        showConfig: false,
        appJiraProject: '',
        appJiraProjectOptions: null
      }
    },
    validations: {
      uploadName: {
        required,
        minLength: minLength(1)
      },
      uploadFile: {
        required
      },
      uploadTool: {
        required
      },
      manualScanName: {
        required,
        minLength: minLength(1)
      },
      manualVulName: {
        required,
        minLength: minLength(1)
      },
      manualCwe: {
        required,
        minLength: minLength(1)
      },
      manualSeverity: {
        required,
        minLength: minLength(1)
      },
      manualOwasp: {
        required,
        minLength: minLength(1)
      },
      manualVulDesc: {
        required,
        minLength: minLength(1)
      },
      manualVulRemedy: {
        required,
        minLength: minLength(1)
      },
      manualVulUrl: {
        required,
        url,
        minLength: minLength(1)
      },
      manualVulParam: {
        required,
        minLength: minLength(1)
      },
      manualVulUrlDesc: {
        required,
        minLength: minLength(1)
      },
      permissionName: {
        required,
        minLength: minLength(1)
      },
      permissionGroup: {
        required,
        minLength: minLength(1)
      },
      allListPermissions: {
        required
      },
      manualVulUrlFile: {
        required
      }
    },
    created() {
      this.param = this.$route.params.applicationId
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.fetchData()
    },
    updated() {
      this.$nextTick(function() {
        if (this.isLoading) {
          this.vulnerabilitiesList = []
          this.openVulCount = 0
          this.closeVulCount = 0
          this.appGrade = 0
          this.highCount = 0
          this.mediumCount = 0
          this.lowCount = 0
          this.infoCount = 0
          this.appSevData = []
          this.chartData = []
          this.fetchData()
          this.isLoading = false
        }
      })
    },
    methods: {
      fetchData() {
        if (this.param && this.org && this.token) {
          axios.get('/applications/' + this.param + '/?scans=1&opened=1&ageing=1&closed=1&avg_ageing=1&severity=1')
            .then(res => {
              for (const ageing of res.data.ageing) {
                this.appSevData.push(ageing)
              }
              this.openVulCount = res.data.open_vul_count
              this.closeVulCount = res.data.closed_vul_count
              this.appGrade = res.data.avg_ageing
              this.appId = res.data.id
              this.appname = res.data.name
              axios.get(res.data.logo)
                .then(res => {
                  this.appLogo = res.data
                }).catch(error => {
                  if (error.res.status === 404) {
                    this.$router.push('/not_found')
                  } else if (error.res.status === 404) {
                    this.$router.push('/forbidden')
                  } else {
                    this.$router.push('/error')
                  }
                })
              this.appUrl = res.data.url
              this.appOsInfo = res.data.os_info
              this.appPlatform = res.data.host_type
              this.highCount = res.data.severity[3] | 0
              this.mediumCount = res.data.severity[2] | 0
              this.lowCount = res.data.severity[1] | 0
              this.infoCount = res.data.severity[0] | 0
              this.chartData.push(
                ['High', this.highCount],
                ['Medium', this.mediumCount],
                ['Low', this.lowCount],
                ['Info', this.infoCount],
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
                  url: 'individual_scan/' + value.fields.id + '/',
                  appDashboard: true
                })
              }
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
      },
      applicationConfigure() {
        if (this.showConfig) {
          this.showConfig = false
        } else {
          this.isLoading = true
          this.showConfig = true
          axios
            .get('/organizations/' + this.org + '/config/')
            .then(res => {
              if (res.data.enable_jira) {
                axios
                  .get('/organizations/' + this.org + '/jira/')
                  .then(res => {
                    axios
                      .get('jira/projects/' + this.param + '/')
                      .then(res => {
                        this.appJiraProjectOptions = res.data
                        this.isLoading = false
                      })
                      .catch(error => {
                        this.isLoading = false
                        if (error.res.status === 404) {
                          this.$router.push('/not_found')
                        } else if (error.res.status === 403) {
                          this.$router.push('/forbidden')
                        } else {
                          this.$router.push('/error')
                        }
                      })
                  })
                  .catch(error => {
                    this.isLoading = false
                    if (error.res.status === 404) {
                      this.$router.push('/not_found')
                    } else if (error.res.status === 403) {
                      this.$router.push('/forbidden')
                    } else {
                      this.$router.push('/error')
                    }
                  })
              }
            })
            .catch(error => {
              this.isLoading = false
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 403) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        }
      },
      submitAppJiraConfig() {
        if (this.param && this.org && this.token) {
          const formData = {
            "name": this.appJiraProject
          }
          axios.put('/applications/' + this.param + '/jira', formData)
            .then(res => {
              this.isLoading = true
              this.$router.push('/projects/individual_application/' + this.param)
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Project',
                text: 'The project has been created Successfully!',
                position: 'top right'
              })
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
      },
      uploadResultsClick() {
        if (this.param && this.org && this.token) {
          axios.get('/tools/')
            .then(res => {
              this.toolOption = []
              for (const value of res.data) {
                this.toolOption.push(value[0])
              }
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
      },
      deleteModal(event) {
        this.$refs.deleteScanModal.show()
        this.deleteScanId = event.id
      },
      closeDeleteScan() {
        this.$refs.deleteScanModal.hide()
      },
      submitDeleteScan() {
        if (this.param && this.org && this.token) {
          axios.delete('/scans/' + this.deleteScanId + '/')
            .then(res => {
              this.isLoading = true
              this.$refs.deleteScanModal.hide()
              this.$router.push('/projects/individual_application/' + this.param)
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
      },
      submitUploadResult() {
        if (this.param && this.org && this.token) {
          const form_data = new FormData()
          form_data.append('file', this.uploadFile)
          form_data.append('name', this.uploadName)
          form_data.append('tool', this.uploadTool)
          axios.post('/applications/' + this.param + '/parsers/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.$router.go('/projects/individual_application/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Application',
                text: 'The file  has been uploaded Successfully!',
                position: 'top right'
              })
              this.uploadFile = ''
              this.uploadName = ''
              this.uploadTool = ''
              this.parsingStatus = res.data.message
              this.parsingScanId = res.data.scan_name
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
      },
      createManualScan() {
        this.manualStepOne = true
      },
      createManualScanStepOne() {
        this.manualStepOne = false
        this.manualStepTwo = true
        this.manualStepThree = false
      },
      prevManualScanStepOne() {
        this.manualStepOne = true
        this.manualStepTwo = false
        this.manualStepThree = false
      },
      createManualScanStepTwo() {
        this.manualStepOne = false
        this.manualStepTwo = false
        this.manualStepThree = true
      },
      prevManualScanStepTwo() {
        this.manualStepOne = false
        this.manualStepTwo = true
        this.manualStepThree = false
      },
      createManualScanWithVul() {
        if (this.param && this.org && this.token) {
          const appId = this.param
          const scanFormData = new FormData()
          scanFormData.append('short_name', this.manualScanName)
          scanFormData.append('application', this.param)
          axios.put('/scans/', scanFormData)
            .then(res => {
              const scanVulFormData = new FormData()
              scanVulFormData.append('name', this.manualVulName)
              scanVulFormData.append('cwe', this.manualCwe)
              scanVulFormData.append('severity', this.manualSeverity.value)
              scanVulFormData.append('owasp', this.manualOwasp)
              scanVulFormData.append('description', this.manualVulDesc)
              scanVulFormData.append('remediation', this.manualVulRemedy)
              scanVulFormData.append('scan', res.data.id)
              axios.put('/vulnerabilities/', scanVulFormData)
                .then(res => {
                  const scanVulEvidFormData = new FormData()
                  scanVulEvidFormData.append('url', this.manualVulUrl)
                  scanVulEvidFormData.append('name', this.manualVulParam)
                  scanVulEvidFormData.append('description', this.manualVulUrlDesc)
                  scanVulEvidFormData.append('file', this.manualVulUrlFile)
                  scanVulEvidFormData.append('vul', res.data.id)
                  axios.put('/evidences/', scanVulEvidFormData, {
                    headers: {
                      'Content-Type': 'multipart/form-data'
                    }
                  })
                    .then(res => {
                      this.isLoading = true
                      this.$router.go('/projects/individual_application/' + appId)
                      this.$notify({
                        group: 'foo',
                        type: 'success',
                        title: 'Application',
                        text: 'The Manual Vulnerability has been created Successfully!',
                        position: 'top right'
                      })
                      this.isLoading = false
                    }).catch(error => {
                      if (error.res.status === 404) {
                        this.$router.push('/not_found')
                      } else if (error.res.status === 404) {
                        this.$router.push('/forbidden')
                      } else {
                        this.$router.push('/error')
                      }
                    })
                  this.$router.go('/projects/individual_application/' + appId)
                }).catch(error => {
                  if (error.res.status === 404) {
                    this.$router.push('/not_found')
                  } else if (error.res.status === 404) {
                    this.$router.push('/forbidden')
                  } else {
                    this.$router.push('/error')
                  }
                })
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        }
      }
    }
  }
</script>
<style scoped>
.btn-orange-close {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;

  }
  .btn-orange-close:focus,
  .btn-orange-close.focus {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-close:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }
  .btn-orange-submit {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;

  }

  .btn-orange-submit:focus,
  .btn-orange-submit.focus {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit:hover {
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

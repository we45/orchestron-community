<template>
    <div>
        <b-container fluid>
           <loading :active.sync="reloadPage" :can-cancel="true"></loading>
            <scan-header :scanHeader="headerData" @addVulnerabilities="addVulnerabilities($event)"></scan-header>
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
                      <!-- <app-bar-chart :barChartData="cweChart" :barChartTitle="'CWE-wise Details'"></app-bar-chart> -->
                       <app-bar-chart v-if="cweListData.length > 0"  :title="'Vulnerabilities by cwe'" :cweData="cweListData" :cweDataRange="cweListDataCounts"></app-bar-chart>
                    </b-col>
                </b-row>
            </b-container>
            <br>
            <vul-table :dataItems="scanVulData"></vul-table>
            <!--Add Vulnerability-->
          <b-modal
                ref="addVulnerabilityModal"
                title="Add Vulnerability"
                size="lg"
                centered>
                <div>
                    <br>
                            <form v-if="manualStepOne">
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Vulnerability Name: *</label></b-col>
                                    <b-col sm="10">
                                      <b-form-input
                                            v-model="manualVulName"
                                            type="text"
                                            class="inline-form-control"
                                            placeholder="Enter Vulnerability Name" :state="!$v.manualVulName.$invalid"></b-form-input>
                                                  <p v-if="error_msgs['vul']" style="text-align:left;" class="error"> * {{ error_msgs['vul_msg']
                        }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">CWE: *</label></b-col>
                                    <b-col sm="10">
                                      <b-form-input
                                            v-model="manualCwe"
                                            type="number"
                                            class="inline-form-control"
                                            placeholder="Enter CWE" :state="!$v.manualCwe.$invalid"></b-form-input>
                                              <p v-if="error_msgs['cwe']" style="text-align:left;" class="error"> * {{ error_msgs['cwe_msg']
                        }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                                <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Severity: *</label></b-col>
                                    <b-col sm="10">
                                      <v-select
                                        :options="manualSeverityList"
                                        v-model="manualSeverity"
                                        placeholder="Select Severity" :state="!$v.manualSeverity.$invalid"></v-select>
                                                                                 <p v-if="error_msgs['sev']" style="text-align:left;" class="error"> * {{ error_msgs['sev_msg']
                        }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">OWASP: *</label></b-col>
                                    <b-col sm="10">
                                      <v-select
                                        :options="manualOwaspList"
                                        v-model="manualOwasp"
                                        placeholder="Select OWASP" :state="!$v.manualOwasp.$invalid"></v-select>
                                          <p v-if="error_msgs['owasp']" style="text-align:left;" class="error"> * {{ error_msgs['owasp_msg']
                        }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                                <br>
                              <b-col cols="12" >
                                <div class="pull-right" style="float: right">
                                    <button type="button"
                                        class="btn btn-orange-close pull-right"
                                        @click=" createManualScanStepOne() " v-if="!$v.manualVulName.$invalid
                                        && !$v.manualCwe.$invalid && !$v.manualSeverity.$invalid && !$v.manualOwasp.$invalid">
                                    Next
                                    </button>
                                </div>
                            </b-col>
                            </form>
                            <form v-if="manualStepTwo">
                              <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Description: *</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulDesc"
                                            type="text"
                                            class="inline-form-control"
                                            :rows="3"
                                            :max-rows="6"
                                            placeholder="Enter Description" :state="!$v.manualVulDesc.$invalid"></b-form-textarea>
                                             <p v-if="error_msgs['desc']" style="text-align:left;" class="error"> * {{ error_msgs['desc_msg']
                        }}</p>
                                    </b-col>
                                </b-row>
                                <br>
                              <b-row class="my-1">
                                    <b-col sm="2"><label class="label">Remediation: *</label></b-col>
                                    <b-col sm="10">
                                      <b-form-textarea
                                            v-model="manualVulRemedy"
                                            type="text"
                                            class="inline-form-control"
                                            :rows="3"
                                            :max-rows="6"
                                            placeholder="Enter Description" :state="!$v.manualVulRemedy.$invalid"></b-form-textarea>
                                            <p v-if="error_msgs['rem']" style="text-align:left;" class="error"> * {{ error_msgs['rem_msg']
                        }}</p>
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
                                    <b-col sm="2"><label class="label">URL: *</label></b-col>
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
                                    <b-col sm="2"><label class="label">Parameter: *</label></b-col>
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
                                    <b-col sm="2"><label class="label">Description: *</label></b-col>
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
                                    <b-col sm="2"><label class="label">File: *</label></b-col>
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
                                        @click="submitAddVulnerabilities() " v-if="!$v.manualVulUrl.$invalid && !$v.manualVulParam.$invalid && !$v.manualVulUrlDesc.$invalid && !$v.manualVulUrlFile.$invalid && validated_evidence_file">
                                    Submit
                                    </button>
                            </form>
                            <br>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeCreateScan() "> Close</button>
                        <!--<button type="button" class="btn btn-orange-submit pull-right" data-dismiss="modal" @click=" submitAddVulnerabilities() " v-if="!$v.projectName.$invalid && !$v.projectLogo.$invalid">-->
                        <!--Submit-->
                        <!--</button>-->
                    </div>
                </b-col>
            </b-modal>
        </b-container>
        <br>
    </div>
</template>

<script>
    import DonutChart from '@/components/Charts/orchyDonutSeverityChart'
    import AppBarChart from '@/components/Charts/chart3DCWE'
    import ScanHeader from '@/components/Scans/Header'
    import VulTable from '@/components/Scans/VulTable'
    import { required, minLength, url, between, integer} from 'vuelidate/lib/validators'
    import axios from '@/utils/auth'
    import { notValidUser } from '@/utils/checkAuthUser'
    import Loading from 'vue-loading-overlay'

    export default {
      name: 'IndividualScan',
      components: {
        DonutChart,
        AppBarChart,
        ScanHeader,
        VulTable,
        Loading
      },
      data() {
        return {
          headerData: [],
          appId: '',
          scanId: '',
          title: 'Vulnerabilities by Severity',
          highCount: 0,
          mediumCount: 0,
          lowCount: 0,
          infoCount: 0,
          chartData: [],
          scanVulData: [],
          cweListData: [],
          cweListDataCounts: [],
          manualVulName: '',
          manualCwe: '',
          manualSeverityList: [{ label: 'High', value: 3 }, { label: 'Medium', value: 2 }, { label: 'Low', value: 1 }, { label: 'Info', value: 0 }],
          manualSeverity: '',
          manualOwaspList: [
            'Injection',
            'Broken Authentication and Session Management',
            'Cross-Site Scripting',
            'Insecure Direct Object References',
            'Security Misconfiguration',
            'Sensitive Data Exposure',
            'Missing Function Level Access Control',
            'Cross-Site Request Forgery',
            'Using Components with Known Vulnerabilities',
            'Unvalidated Redirects and Forwards',
            'Uncategorized'
        ],
        error_msgs: {
          'scan': false,
          'scan_msg': '',
          'vul': false,
          'vul_msg': '',
          'cwe': false,
          'cwe_msg': '',
          'sev': false,
          'sev_msg': '',
          'owasp': false,
          'owasp_msg': '',
          'desc': false,
          'desc_msg': '',
          'rem': false,
          'rem_msg': '',
          'manual': false,
          'manual_msg': ''
        },
          manualOwasp: '',
          manualStepOne: false,
          manualStepTwo: false,
          reloadPage: false,
          manualVulDesc: '',
          manualVulRemedy: '',
          manualStepThree: false,
          manualVulUrl: '',
          manualVulParam: '',
          manualVulUrlDesc: '',
          manualVulUrlFile: '',
          validated_evidence_file: false,
          cweChart: []
        }
      },
      validations: {
        manualVulName: {
          required,
          minLength: minLength(1)
        },
        manualCwe: {
          required,
          minLength: minLength(1),
          integer,
          between: between(0, 1000)
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
        manualVulUrlFile: {
          required
        }
      },
      created() {
        this.org = localStorage.getItem('org')
        this.token = localStorage.getItem('token')
        this.param = this.$route.params.scanId
        this.fetchData()
      },
      watch: {
        'manualVulUrlFile': function(value_name) {
            var ext = value_name.name.split(".")
            var realData = ext[(ext.length)-1]
            var validated_data =  ['png','jpg','jpeg','bmp','gif','tiff']
            var data_form_submit = validated_data.includes(realData);
            var size_of_file = 1024 * 1024 * 20
            if(data_form_submit &&  (value_name.size < size_of_file)){
                this.validated_evidence_file = true
            }
            else{
                this.validated_evidence_file = false
            }
        },
          'manualScanName': function(value_name) {
        if (value_name.length > 255) {
          this.error_msgs['manual'] = true
          this.error_msgs['manual_msg'] = 'Max Length is 255 Characters'
        } else {
          this.error_msgs['manual'] = false
        }
      },
      'manualVulName': function(value_name) {
        if (value_name.length > 255) {
          this.error_msgs['vul'] = true
          this.error_msgs['vul_msg'] = 'Max Length is 255 Characters'
          } else {
            this.error_msgs['vul'] = false
          }
        },
      },
      methods: {
        fetchData() {
          this.reloadPage = true
          if (this.org && this.token) {
            axios.get('/scans/' + this.param + '/?stats=1&vuls=1')
              .then(res => {
                this.cweListData = []
                this.cweListDataCounts = []
                this.headerData.push({
                  'scanCreatedBy': res.data.triggered_by,
                  'appName': res.data.application_name,
                  'name': res.data.short_name,
                  'tool': res.data.tool,
                  'date': res.data.created_on
                })
                for (const [key, val] of Object.entries(res.data.cwe)) {
                  this.cweChart.push([key, val])
                  this.cweListData.push(parseInt(val))
                  this.cweListDataCounts.push(parseInt(key))
                }
                this.highCount = res.data.severity[3] | 0
                this.mediumCount = res.data.severity[2] | 0
                this.lowCount = res.data.severity[1] | 0
                this.infoCount = res.data.severity[0] | 0
                this.scanId = res.data.id
                this.appId = res.data.application
                this.chartData.push(
                  ['High', this.highCount],
                  ['Medium', this.mediumCount],
                  ['Low', this.lowCount],
                  ['Info', this.infoCount],
                )
                for (const vul of res.data.vuls) {
                  for (const val of Object.values(vul)) {
                    this.scanVulData.push({
                      sev: val.severity,
                      name: val.name,
                      cwe: val.cwe,
                      id: val.id,
                      url: '/projects/individual_application/' + this.appId + '/individual_scan/' + this.scanId + '/individual_vul/' + val.id + '/'
                      
                    })
                  }
                }
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
        closeCreateScan(){
          this.$refs.addVulnerabilityModal.hide()
        },
        addVulnerabilities() {
          this.$refs.addVulnerabilityModal.show()
          this.manualStepOne = true
        },
        createManualScanStepOne() {
          this.$refs.addVulnerabilityModal.show()
          this.manualStepOne = false
          this.manualStepTwo = true
          this.manualStepThree = false
        },
        prevManualScanStepOne() {
          this.$refs.addVulnerabilityModal.show()
          this.manualStepOne = true
          this.manualStepTwo = false
          this.manualStepThree = false
        },
        createManualScanStepTwo() {
          this.$refs.addVulnerabilityModal.show()
          this.manualStepOne = false
          this.manualStepTwo = false
          this.manualStepThree = true
        },
        prevManualScanStepTwo() {
          this.$refs.addVulnerabilityModal.show()
          this.manualStepOne = false
          this.manualStepTwo = true
          this.manualStepThree = false
        },
        submitAddVulnerabilities() {
          if (this.org && this.token) {
            const scanVulFormData = new FormData()
            scanVulFormData.append('name', this.manualVulName)
            scanVulFormData.append('cwe', this.manualCwe)
            scanVulFormData.append('severity', this.manualSeverity.value)
            scanVulFormData.append('owasp', this.manualOwasp)
            scanVulFormData.append('description', this.manualVulDesc)
            scanVulFormData.append('remediation', this.manualVulRemedy)
            scanVulFormData.append('scan', this.param)
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
                    this.$refs.addVulnerabilityModal.hide()
                    this.$router.go('/projects/individual_application/'+ this.appId  + '/individual_scan/'+ this.scanId +'/' )
                    this.$notify({
                      group: 'foo',
                      type: 'success',
                      title: 'success',
                      text: 'The manual vulnerability has been created successfully!',
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
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 403) {
                  this.$router.push('/forbidden')
                }
                else if (error.response.status === 400) {
                    if (error.response.data['name']) {
                      this.error_msgs['vul'] = true
                      this.error_msgs['vul_msg'] = error.response.data['name'][0]
                    }
                    if (error.response.data['cwe']) {
                      this.error_msgs['cwe'] = true
                      this.error_msgs['cwe_msg'] = error.response.data['cwe'][0]
                    }
                    if (error.response.data['severity']) {
                      this.error_msgs['sev'] = true
                      this.error_msgs['sev_msg'] = error.response.data['severity'][0]
                    }
                    if (error.response.data['owasp']) {
                      this.error_msgs['owasp'] = true
                      this.error_msgs['owasp_msg'] = error.response.data['owasp'][0]
                    }
                    if (error.response.data['description']) {
                      this.error_msgs['desc'] = true
                      this.error_msgs['desc_msg'] = error.response.data['description'][0]
                    }
                    if (error.response.data['remediation']) {
                      this.error_msgs['rem'] = true
                      this.error_msgs['rem_msg'] = error.response.data['remediation'][0]
                    }
                  } 
                 else {
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
</style>

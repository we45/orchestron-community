<template>
  <div>
   		<loading :active.sync="reloadPage" :can-cancel="true"></loading>
      <b-container fluid >
	    <b-container fluid style="background-color: #FFFFFF;">
		    <b-container fluid style="background-color: #FFFFFF;">
		        <br>
		        <br>
		        <b-row>
		        	<b-col cols="6">
			            <label for="">Select Report Scope</label>
			            <v-select v-model="reportScope" :options="reportScopeOptions"
			                      placeholder="Select Scope" @input="reportSelectedScope(reportScope)"></v-select>
			        </b-col>

			        <b-col cols="6">
		            <label for="">Report/Action Type</label>
		               <v-select v-model="reportType" :options="reportTypeOptions" placeholder="Select Type"
                      @input="reportSelectedType(reportType)"></v-select>
		          </b-col>
		        </b-row>
		        <br>
		        <br>

        <b-row>
          <b-col cols="1">
            <label>Filters : </label>
          </b-col>
          <b-col cols="11">
            <v-select
                  multiple
                  :options="filterOptions"
                  label="label"
                  v-model="selectedOption"
                  placeholder="Filter"
                  style="font-family: Avenir;"
                  @input="reportFilters"
                  ></v-select>
          </b-col>
        </b-row>


        <br>
        <br>


		    </b-container>

		         <!--Applications-->
	          <b-modal ref="appModal" hide-footer title="Select Application" centered>
	            <div>
	              <form @submit.prevent="submitSelectedApplications">
	                <label for="">Select Application</label>
	                <b-col>

	                  <template >
	                    <v-select
	                      placeholder="Select Applications"
	                      :options="filterAppOpt"
	                      v-model="filterAppModel"
	                      multiple="multiple">
	                    </v-select>
	                  </template>
	                </b-col>
	                <br>
	                <hr>
	                <div class="pull-right">
	                  <template>
	                    <button
	                      type="button"
	                      class="btn btn-orange-submit"
	                      data-dismiss="modal"
	                      @click=" submitSelectedApplications() "
	                      style="float: right">
	                      Submit
	                    </button>
	                  </template>
	                  <button type="button" class="btn btn-orange-close" @click=" closeApplicationModal()"
	                          style="float: right">Cancel
	                  </button>
	                </div>
	              </form>
	            </div>
	          </b-modal>


	            <!--Tools-->

		          <b-modal ref="toolModal" hide-footer title="Select Tool" centered>
		            <div>
		              <form @submit.prevent="submitSelectedTool">
		                <label for="">Select Tool</label>
		                <b-col>
		                  <v-select
		                    placeholder="Select Tool"
		                    :options="filterToolOpt"
		                    v-model="filterToolModel"
		                    multiple="multiple">
		                  </v-select>
		                </b-col>
		                <br>
		                <hr>
		                <div class="pull-right">
		                  <button type="button" class="btn btn-orange-submit" data-dismiss="modal"
		                          @click=" submitSelectedTool() " style="float: right">
		                    Submit
		                  </button>
		                  <button type="button" class="btn btn-orange-close" @click=" closeToolModal()" style="float: right">
		                    Cancel
		                  </button>
		                </div>
		              </form>
		            </div>
		          </b-modal>


		                    <!--Severity-->

		          <b-modal ref="sevModal" hide-footer title="Select Severity" centered>
		            <div>
		              <form @submit.prevent="submitSelectedSeverity">
		                <label for="">Select Severity</label>
		                <b-col>
		                  <v-select
		                    placeholder="Select Severity"
		                    :options="filterSevOpt"
		                    v-model="filterSevModel"
		                    multiple="multiple">
		                  </v-select>
		                </b-col>
		                <br>
		                <hr>
		                <div class="pull-right">
		                  <button type="button" class="btn btn-orange-submit" data-dismiss="modal"
		                          @click=" submitSelectedSeverity() " style="float: right">
		                    Submit
		                  </button>
		                  <button type="button" class="btn btn-orange-close" @click=" closeSeverityModal()"
		                          style="float: right">Cancel
		                  </button>
		                </div>
		              </form>
		            </div>
		          </b-modal>


               <!--Engagement-->

          <b-modal ref="engagementModal" hide-footer title="Select Engagement" centered>
            <div>
              <form @submit.prevent="submitSelectedEngagement">
                <label for="">Select Engagement</label>
                <b-col>
                  <v-select
                    placeholder="Select Engagement"
                    :options="filterEngagementOpt"
                    v-model="filterEngModel"
                    multiple="multiple">
                  </v-select>
                </b-col>
                <br>
                <hr>
                <div class="pull-right">
                    <button
                      type="button"
                      class="btn btn-orange-submit"
                      data-dismiss="modal"
                      @click=" submitSelectedEngagement() "
                      style="float: right">
                      Submit
                    </button>
                  <button type="button" class="btn btn-orange-close" @click=" closeEngagementModal()"
                          style="float: right">Cancel
                  </button>
                </div>
              </form>
            </div>
          </b-modal>
          <template v-if="reportType.value==='execSummary' ">

  		          <excutive-report :excutivedata="excutivedata"
                             :excutiveSeverityChartData="excutiveSeverityChartData"
                             :excutiveVulDataItems="excutiveVulDataItems"
                             :excutiveHighCount="excutiveHighCount"
                             :excutiveMediumCount="excutiveMediumCount"
                             :excutiveLowCount="excutiveLowCount"
                             :excutiveInfoCount="excutiveInfoCount"
                             :excutiveVulAgeingData="excutiveVulAgeingData"
                             :excutiveVulAgeingCategories="excutiveVulAgeingCategories"
                             :excutiveVulAgeingSubTitle="excutiveVulAgeingSubTitle"
                             :excutiveNoPages="excutiveNoPages"
                             @clickPagination="clickExcutivePagination($event)"
                             :excutiveOwaspCategory="excutiveOWASPCategory"
                             :excutiveOwaspchartData="excutiveOwaspchartData"
                             :excutiveVulAgeingOptions="excutiveVulAgeingOptions"
                             :excutiveowaspOptions="excutiveowaspOptions"></excutive-report>
          </template>

		</b-container>
  </b-container>
	</div>
</template>

<script>
import axios from '@/utils/auth'
import excutiveReport from '@/components/Reporting/excutiveReport'
import Loading from 'vue-loading-overlay'
  export default {
    name: 'ReportView',
    components: {
      excutiveReport,
      Loading
    },
    data() {
      return {
        excutiveVulDataItems: [],
      	msg: '',
      	reportScope: '',
        filterAppModel: '',
        excutiveVulAgeingSubTitle: '',
      	isLoading: false,
        reloadPage: false,
      	reportScopeOptions: [
          // { label: 'Project', value: 'project' },
          {label: 'Application', value: 'application'},
          // {label: 'Engagement', value: 'engagement'}
        ],
        reportTypeOptions: [{label: 'Exec Summary', value: 'execSummary'},
            // {label: 'Detailed Report', value: 'detailedReport'}
            ],
      	filterOptions:[
      		 {
                label: 'Application Filter',
                value: 'appFilter'
              },
              {
                label: 'Severity Filter',
                value: 'sevFilter'
              },
              {
                label: 'Tool Filter',
                value: 'toolFilter'
              }
            ],
        selectedOption: '',
        data_values_selected: {},
        filterAppOpt: [],
        filterToolOpt: [],
        filterEngagementOpt: [],
        filterToolModel: '',
        reportType: '',
		filterSevOpt: [
				{label: 'High', value: 3},
                {label: 'Medium', value: 2},
                {label: 'Low', value: 1},
                {label: 'Info', value: 0}],
		filterSevModel: '',
		highLable: 'High',
        mediumLable: 'Medium',
        lowLable: 'Low',
        infoLable: 'Info',
        filterEngModel: '',
        excutiveNoPages: 0,
          excutivedata: [],
          excutiveSeverityChartData: [],
          excutiveVulAgeingData: [],
          excutiveVulAgeingCategories: [],
          excutiveOWASPCategory: [],
          excutiveOwaspchartData:[],
          excutiveVulAgeingOptions: {},
          excutiveowaspOptions: {},
          excutiveHighCount: 0,
          excutiveMediumCount: 0,
          excutiveLowCount: 0,
          excutiveInfoCount: 0,

      	}
      },
    methods: {
      emptyChanges(){
          this.excutiveNoPages=0
          this.excutivedata=[]
          this.excutiveSeverityChartData=[]
          this.excutiveVulAgeingData=[]
          this.excutiveVulAgeingCategories=[]
          this.excutiveOWASPCategory=[]
          this.excutiveOwaspchartData=[]
          this.excutiveVulAgeingOptions={}
          this.excutiveowaspOptions={}
          this.excutiveHighCount=0
          this.excutiveMediumCount=0
          this.excutiveLowCount=0
          this.excutiveInfoCount=0
          this.filterEngModel = ''
          this.filterToolModel = ''
          this.filterSevModel = ''
          this.filterAppModel = ''
          this.excutiveVulDataItems = []
          this.excutiveVulAgeingSubTitle  = ''

      },
    reportSelectedScope(reportScope) {
        this.emptyChanges()
        // this.reportTypeOptions = []
        this.reportType = false
        this.filterOptions = []
        this.selectedOption = []
        const currentVal = this.reportScope.value

        if (currentVal === 'application') {
            this.filterOptions.push(
              {
                label: 'Application Filter',
                value: 'appFilter'
              },
              {
                label: 'Severity Filter',
                value: 'sevFilter'
              },
              {
                label: 'Tool Filter',
                value: 'toolFilter'
              }
            )
        }
      },
    closeApplicationModal() {
        this.$refs.appModal.hide()
    },
    closeToolModal() {
        this.$refs.toolModal.hide()
    },
    submitSelectedApplications() {
	    this.selectedOption = this.selectedOption.filter(function (item) {
			return item.label !== 'app:' + item.label
		})

		if (Array.isArray(this.filterAppModel)) {
				this.selectedOption = []
				if (Array.isArray(this.filterSevModel)) {
					for (const sevs of this.filterSevModel) {
						this.selectedOption.push({label: 'sev:' + sevs.label, value: sevs.value})
					}
				}
				if (Array.isArray(this.filterToolModel)) {
					for (const tools of this.filterToolModel) {
						this.selectedOption.push({label: 'tool:' + tools.label, value: tools.value})
					}
				}
				for (const apps of this.filterAppModel) {
					this.selectedOption.push({label: 'app:' + apps.label, value: apps.value})
				}
			}
			else {
				this.selectedOption.push({label: 'app:' + this.filterAppModel.label, value: this.filterAppModel.value})
			}
			this.selectedOption = this.selectedOption.filter(function (item) {
				return item.value !== 'appFilter'
			})
			this.$refs.appModal.hide()
    },

    submitSelectedTool() {
        this.selectedOption = this.selectedOption.filter(function (item) {
          return item.label !== 'tool:' + item.label
        })

        if (Array.isArray(this.filterToolModel)) {
          this.selectedOption = []

           if(this.reportScope.value === 'application'){
              if (Array.isArray(this.filterAppModel)) {
                for (const apps of this.filterAppModel) {
                  this.selectedOption.push({label: 'app:' + apps.label, value: apps.value})
                }
              }
            }
          if (Array.isArray(this.filterSevModel)) {
            for (const sevs of this.filterSevModel) {
              this.selectedOption.push({label: 'sev:' + sevs.label, value: sevs.value})
            }
          }

          if(this.reportScope.value === 'engagement'){
            if (Array.isArray(this.filterEngModel)) {
                for (const eng of this.filterEngModel) {
                  this.selectedOption.push({label: 'eng:' + eng.label, value: eng.value})
                }
            }
          }

          if (Array.isArray(this.filterProjectModel)) {
            for (const projects of this.filterProjectModel) {
              this.selectedOption.push({label: 'proj:' + projects.label, value: projects.value})
            }
          }

          for (const tools of this.filterToolModel) {
            this.selectedOption.push({label: 'tool:' + tools.label, value: tools.value})
          }
        } else {
          this.selectedOption.push({label: 'tool:' + this.filterToolModel.label, value: this.filterToolModel.value})
        }

        this.selectedOption = this.selectedOption.filter(function (item) {
          return item.value !== 'toolFilter'
        })
        this.$refs.toolModal.hide()
      },


    submitSelectedSeverity() {
        this.selectedOption = this.selectedOption.filter(function (item) {
          return item.label !== 'sev:' + item.label
        })
        if (Array.isArray(this.filterSevModel)) {
          this.selectedOption = []
          if(this.reportScope.value === 'application'){
              if (Array.isArray(this.filterAppModel)) {
                for (const apps of this.filterAppModel) {
                  this.selectedOption.push({label: 'app:' + apps.label, value: apps.value})
                }
              }
            }
          if (Array.isArray(this.filterToolModel)) {
            for (const tools of this.filterToolModel) {
              this.selectedOption.push({label: 'tool:' + tools.label, value: tools.value})
            }
          }
          for (const sevs of this.filterSevModel) {
            this.selectedOption.push({label: 'sev:' + sevs.label, value: sevs.value})
          }

         if(this.reportScope.value === 'engagement'){
            if (Array.isArray(this.filterEngModel)) {
                for (const eng of this.filterEngModel) {
                  this.selectedOption.push({label: 'eng:' + eng.label, value: eng.value})
                }
            }
          }


          if (Array.isArray(this.filterProjectModel)) {
            for (const projects of this.filterProjectModel) {
              this.selectedOption.push({label: 'proj:' + projects.label, value: projects.value})
            }
          }
        } else {
          this.selectedOption.push({label: 'app:' + this.filterAppModel.label, value: this.filterAppModel.value})
        }
        this.selectedOption = this.selectedOption.filter(function (item) {
          return item.value !== 'sevFilter'
        })
        this.$refs.sevModal.hide()
      },

      closeSeverityModal() {
        this.$refs.sevModal.hide()
      },

      clickExcutivePagination(event){
        if (event.page > 1) {
             axios.post('/report/executive/?page=' + event.page, this.data_values_selected)
              .then(res => {
                this.excutiveNoPages = res.data.open_vul_count
              this.excutivedata = []
              this.excutivedata = res.data
              this.excutiveSeverityChartData = []
              this.excutiveVulAgeingData = []
              this.excutiveVulAgeingCategories = []
              this.excutiveOWASPCategory = []
              this.excutiveOwaspchartData = []
              this.excutiveVulAgeingOptions = {}
              this.excutiveowaspOptions = {}
              this.excutiveHighCount = 0
              this.excutiveMediumCount = 0
              this.excutiveLowCount = 0
              this.excutiveInfoCount = 0
              this.excutiveHighCount = this.excutivedata.severity[3] | 0
              this.excutiveMediumCount = this.excutivedata.severity[2] | 0
              this.excutiveLowCount = this.excutivedata.severity[1] | 0
              this.excutiveInfoCount = this.excutivedata.severity[0] | 0
              console.log("res data", res.data.owasp)
              this.excutiveVulDataItems = []
              for (var vuls of res.data.open_vuls) {
                const vulName = vuls.common_name
                const vulSev = vuls.severity
                const vulApps = vuls.apps
                const cwe = parseInt(vuls.cwe)
                // console.log("vulname", vulName)
                 this.excutiveVulDataItems.push(
                    {
                      vulnerability: vuls.common_name,
                      application: vuls.apps,
                      severity: vuls.severity,
                      cwe: cwe
                    }
                  )


                // const reopen_cnt = parseInt(vuls.reopen_count)

              }
              this.excutiveSeverityChartData.push(
                [this.highLable, this.excutivedata.severity[3] | 0],
                [this.mediumLable, this.excutivedata.severity[2] | 0],
                [this.lowLable, this.excutivedata.severity[1] | 0],
                [this.infoLable, this.excutivedata.severity[0] | 0]
              )
              const highAgeingSevCount = []
              const mediumAgeingSevCount = []
              const lowAgeingSevCount = []
              const infoAgeingSevCount = []
              console.log("hereeee",res.data.ageing)
              for (const [key, value] of Object.entries(res.data.ageing)) {
                  console.log("keysssssss", key)
                for (const [keys, values] of Object.entries(value)) {
                  this.excutiveVulAgeingCategories.push(keys)
                  highAgeingSevCount.push(values[3])
                  mediumAgeingSevCount.push(values[2])
                  lowAgeingSevCount.push(values[1])
                  infoAgeingSevCount.push(values[0])
                  // this.excutiveVulAgeingCategories = ['0-5 days', '6-10 days', '11-20 days', '21-40 days', '41-80 days', '81-100 days', 'More than 100 days']
                  // this.excutiveVulAgeingCategories.push(ageing)
                }
              }


              this.excutiveVulAgeingData.push(
                {
                  name: this.infoLable,
                  data: infoAgeingSevCount,
                  color: '#1d1e52'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.lowLable,
                  data: lowAgeingSevCount,
                  color: '#008b8f'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.mediumLable,
                  data: mediumAgeingSevCount,
                  color: '#ff9c2c'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.highLable,
                  data: highAgeingSevCount,
                  color: '#d11d55'
                }
              )


              this.excutiveVulAgeingOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveVulAgeingCategories
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveVulAgeingData
              }

              this.excutiveVulAgeingSubTitle = res.data.entry_date || ''

              const highSevCount = []
              const mediumSevCount = []
              const lowSevCount = []
              const infoSevCount = []
              console.log("heree")
              for (const [key, value] of Object.entries(res.data.owasp)) {
                // console.log("owasppp", key)
                this.excutiveOWASPCategory.push(key)
                highSevCount.push(value[3])
                mediumSevCount.push(value[2])
                lowSevCount.push(value[1])
                infoSevCount.push(value[0])
              }


              this.excutiveOwaspchartData.push(
                {
                  name: this.infoLable,
                  data: infoSevCount,
                  color: '#1d1e52'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.lowLable,
                  data: lowSevCount,
                  color: '#008b8f'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.mediumLable,
                  data: mediumSevCount,
                  color: '#ff9c2c'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.highLable,
                  data: highSevCount,
                  color: '#d11d55'
                }
              )

              this.excutiveowaspOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveOWASPCategory
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveOwaspchartData
              }

                 })
              .catch(error => {
                if (error.response.data.detail === 'Signature has expired.') {
                  notValidUser()
                  this.$router.push('/')
                }
              })
        }
        else{
           axios.post('/report/executive/', this.data_values_selected)
            .then(res => {
              // console.log("hereeeeeee")
              this.excutiveNoPages = res.data.open_vul_count
              this.excutivedata = []
              this.excutivedata = res.data
              this.excutiveSeverityChartData = []
              this.excutiveVulAgeingData = []
              this.excutiveVulAgeingCategories = []
              this.excutiveOWASPCategory = []
              this.excutiveOwaspchartData = []
              this.excutiveVulAgeingOptions = {}
              this.excutiveowaspOptions = {}
              this.excutiveHighCount = 0
              this.excutiveMediumCount = 0
              this.excutiveLowCount = 0
              this.excutiveInfoCount = 0
              this.excutiveHighCount = this.excutivedata.severity[3] | 0
              this.excutiveMediumCount = this.excutivedata.severity[2] | 0
              this.excutiveLowCount = this.excutivedata.severity[1] | 0
              this.excutiveInfoCount = this.excutivedata.severity[0] | 0
              console.log("res data", res.data.owasp)
              this.excutiveVulDataItems = []
              for (var vuls of res.data.open_vuls) {
                const vulName = vuls.common_name
                const vulSev = vuls.severity
                const vulApps = vuls.apps
                const cwe = parseInt(vuls.cwe)
                // console.log("vulname", vulName)
                 this.excutiveVulDataItems.push(
                    {
                      vulnerability: vuls.common_name,
                      application: vuls.apps,
                      severity: vuls.severity,
                      cwe: cwe
                    }
                  )


                // const reopen_cnt = parseInt(vuls.reopen_count)

              }
              this.excutiveSeverityChartData.push(
                [this.highLable, this.excutivedata.severity[3] | 0],
                [this.mediumLable, this.excutivedata.severity[2] | 0],
                [this.lowLable, this.excutivedata.severity[1] | 0],
                [this.infoLable, this.excutivedata.severity[0] | 0]
              )
              const highAgeingSevCount = []
              const mediumAgeingSevCount = []
              const lowAgeingSevCount = []
              const infoAgeingSevCount = []
              console.log("hereeee",res.data.ageing)
              for (const [key, value] of Object.entries(res.data.ageing)) {
                  console.log("keysssssss", key)
                for (const [keys, values] of Object.entries(value)) {
                  this.excutiveVulAgeingCategories.push(keys)
                  highAgeingSevCount.push(values[3])
                  mediumAgeingSevCount.push(values[2])
                  lowAgeingSevCount.push(values[1])
                  infoAgeingSevCount.push(values[0])
                  // this.excutiveVulAgeingCategories = ['0-5 days', '6-10 days', '11-20 days', '21-40 days', '41-80 days', '81-100 days', 'More than 100 days']
                  // this.excutiveVulAgeingCategories.push(ageing)
                }
              }


              this.excutiveVulAgeingData.push(
                {
                  name: this.infoLable,
                  data: infoAgeingSevCount,
                  color: '#1d1e52'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.lowLable,
                  data: lowAgeingSevCount,
                  color: '#008b8f'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.mediumLable,
                  data: mediumAgeingSevCount,
                  color: '#ff9c2c'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.highLable,
                  data: highAgeingSevCount,
                  color: '#d11d55'
                }
              )


              this.excutiveVulAgeingOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveVulAgeingCategories
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveVulAgeingData
              }

              this.excutiveVulAgeingSubTitle = res.data.entry_date || ''

              const highSevCount = []
              const mediumSevCount = []
              const lowSevCount = []
              const infoSevCount = []
              console.log("heree")
              for (const [key, value] of Object.entries(res.data.owasp)) {
                // console.log("owasppp", key)
                this.excutiveOWASPCategory.push(key)
                highSevCount.push(value[3])
                mediumSevCount.push(value[2])
                lowSevCount.push(value[1])
                infoSevCount.push(value[0])
              }


              this.excutiveOwaspchartData.push(
                {
                  name: this.infoLable,
                  data: infoSevCount,
                  color: '#1d1e52'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.lowLable,
                  data: lowSevCount,
                  color: '#008b8f'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.mediumLable,
                  data: mediumSevCount,
                  color: '#ff9c2c'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.highLable,
                  data: highSevCount,
                  color: '#d11d55'
                }
              )

              this.excutiveowaspOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveOWASPCategory
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveOwaspchartData
              }
            })
            .catch(error => {
              console.log("errrr", error)
              if (error.response.data.detail === 'Signature has expired.') {
                notValidUser()
                this.$router.push('/')
              }
            })
        }
      },
    reportFilters(filterValue) {
        // if (filterValue.length > 0) {
          const currentFilter = filterValue[filterValue.length - 1].value
          // console.log("tooooooooolll", currentFilter)
          if(currentFilter === 'toolFilter'){
          	// window.alert("tool")
          }
          this.data_values_selected = {'apps': [], 'eng': [], 'proj': [], 'sev': [], 'tools': []}
          for (const selOpt of this.selectedOption) {
            if (selOpt.label.includes('app:')) {
              this.data_values_selected['apps'].push(selOpt.value)
            }
            if (selOpt.label.includes('sev:')) {
              this.data_values_selected['sev'].push(selOpt.value)
            }
            if (selOpt.label.includes('tool:')) {
              this.data_values_selected['tools'].push(selOpt.label.split(':').slice(1, 2)[0])
            }
            if (selOpt.label.includes('proj:')) {
              this.data_values_selected['proj'].push(selOpt.value)
            }
            if (selOpt.label.includes('eng:')) {
              this.data_values_selected['eng'].push(selOpt.value)
            }
          }
          // Application filter
          if (currentFilter === 'appFilter') {
            axios.get('/applications/list/')
              .then(res => {
              	this.filterAppOpt = []
                for (const app of res.data) {
                    this.filterAppOpt.push({label: app.name, value: app.id})
                }
              })
              .catch(error => {
              })

            this.$refs.appModal.show()
          } else {
            this.$refs.appModal.hide()
          }

          // Severity Filter
          if (currentFilter === 'sevFilter') {
            this.$refs.sevModal.show()
          } else {
            this.$refs.sevModal.hide()
          }


          if (currentFilter === 'toolFilter') {
            axios.get('/tools/')
              .then(res => {
                this.filterToolOpt = []
                for (const tool of res.data) {
                  this.filterToolOpt.push({label: tool[0], value: tool[1]})
                }
              })
              .catch(error => {
                if (error.response.data.detail === 'Signature has expired.') {
                  notValidUser()
                  this.$router.push('/')
                }
              })
            this.$refs.toolModal.show()
          } else {
            this.$refs.toolModal.hide()
          }


          // Engagement Filter
          if (currentFilter === 'engFilter') {
            axios.get('/engagements/')
              .then(res => {
              	this.filterEngagementOpt  = []
                for (const engagement of res.data.results) {
                    this.filterEngagementOpt.push({label: engagement.name, value: engagement.id})
                }
              })
              .catch(error => {
                if (error.response.data.detail === 'Signature has expired.') {
                  notValidUser()
                  this.$router.push('/')
                }
              })
            this.$refs.engagementModal.show()
          } else {
            this.$refs.engagementModal.hide()
          }



          if (filterValue.length > 0) {
            if (this.reportType.value === 'execSummary' || this.reportType.value === 'detailedReport') {
          axios.post('/report/executive/', this.data_values_selected)
            .then(res => {
              this.reloadPage = true
            	// console.log("hereeeeeee")
              this.excutiveNoPages = res.data.open_vul_count
              this.excutivedata = []
              this.excutivedata = res.data
              this.excutiveSeverityChartData = []
              this.excutiveVulAgeingData = []
              this.excutiveVulAgeingCategories = []
              this.excutiveOWASPCategory = []
              this.excutiveOwaspchartData = []
              this.excutiveVulAgeingOptions = {}
              this.excutiveowaspOptions = {}
              this.excutiveHighCount = 0
              this.excutiveMediumCount = 0
              this.excutiveLowCount = 0
              this.excutiveInfoCount = 0
              this.excutiveHighCount = this.excutivedata.severity[3] | 0
              this.excutiveMediumCount = this.excutivedata.severity[2] | 0
              this.excutiveLowCount = this.excutivedata.severity[1] | 0
              this.excutiveInfoCount = this.excutivedata.severity[0] | 0
              console.log("res data", res.data.owasp)
              this.excutiveVulDataItems = []
              for (var vuls of res.data.open_vuls) {
                const vulName = vuls.common_name
                const vulSev = vuls.severity
                const vulApps = vuls.apps
                const cwe = parseInt(vuls.cwe)
                // console.log("vulname", vulName)
                 this.excutiveVulDataItems.push(
                    {
                      vulnerability: vuls.common_name,
                      application: vuls.apps,
                      severity: vuls.severity,
                      cwe: cwe
                    }
                  )


                // const reopen_cnt = parseInt(vuls.reopen_count)

              }
              this.excutiveSeverityChartData.push(
                [this.highLable, this.excutivedata.severity[3] | 0],
                [this.mediumLable, this.excutivedata.severity[2] | 0],
                [this.lowLable, this.excutivedata.severity[1] | 0],
                [this.infoLable, this.excutivedata.severity[0] | 0]
              )
              const highAgeingSevCount = []
              const mediumAgeingSevCount = []
              const lowAgeingSevCount = []
              const infoAgeingSevCount = []
              for (const [key, value] of Object.entries(res.data.ageing)) {
                  // console.log("keysssssss", key)
                for (const [keys, values] of Object.entries(value)) {
                  this.excutiveVulAgeingCategories.push(keys)
                  highAgeingSevCount.push(values[3])
                  mediumAgeingSevCount.push(values[2])
                  lowAgeingSevCount.push(values[1])
                  infoAgeingSevCount.push(values[0])
                  // this.excutiveVulAgeingCategories = ['0-5 days', '6-10 days', '11-20 days', '21-40 days', '41-80 days', '81-100 days', 'More than 100 days']
                  // this.excutiveVulAgeingCategories.push(ageing)
                }
              }


              this.excutiveVulAgeingData.push(
                {
                  name: this.infoLable,
                  data: infoAgeingSevCount,
                  color: '#1d1e52'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.lowLable,
                  data: lowAgeingSevCount,
                  color: '#008b8f'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.mediumLable,
                  data: mediumAgeingSevCount,
                  color: '#ff9c2c'
                }
              )
              this.excutiveVulAgeingData.push(
                {
                  name: this.highLable,
                  data: highAgeingSevCount,
                  color: '#d11d55'
                }
              )


              this.excutiveVulAgeingOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveVulAgeingCategories
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveVulAgeingData
              }

              this.excutiveVulAgeingSubTitle = res.data.entry_date || ''

              const highSevCount = []
              const mediumSevCount = []
              const lowSevCount = []
              const infoSevCount = []
              console.log("heree")
              for (const [key, value] of Object.entries(res.data.owasp)) {
                // console.log("owasppp", key)
                this.excutiveOWASPCategory.push(key)
                highSevCount.push(value[3])
                mediumSevCount.push(value[2])
                lowSevCount.push(value[1])
                infoSevCount.push(value[0])
              }


              this.excutiveOwaspchartData.push(
                {
                  name: this.infoLable,
                  data: infoSevCount,
                  color: '#1d1e52'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.lowLable,
                  data: lowSevCount,
                  color: '#008b8f'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.mediumLable,
                  data: mediumSevCount,
                  color: '#ff9c2c'
                }
              )

              this.excutiveOwaspchartData.push(
                {
                  name: this.highLable,
                  data: highSevCount,
                  color: '#d11d55'
                }
              )

              this.excutiveowaspOptions = {
                chart: {
                  type: 'bar'
                },
                title: {
                  text: ''
                },
                credits: {
                  enabled: false
                },
                xAxis: {
                  categories: this.excutiveOWASPCategory
                },
                yAxis: {
                  min: 0,
                  title: {
                    text: 'Count'
                  }
                },
                legend: {
                  reversed: true
                },
                plotOptions: {
                  series: {
                    stacking: 'normal'
                  }
                },
                series: this.excutiveOwaspchartData
              }
              this.reloadPage = false
            })
            .catch(error => {
              this.reloadPage = false
            	console.log("errrr", error)
              if (error.response.data.detail === 'Signature has expired.') {
                notValidUser()
                this.$router.push('/')
              }
            })
        }
        }
      }
        // }
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

  .label-style-head {
    font-size: 18px;
  }

  .data-points {
    padding: 6px;
    margin-bottom: 0px;
    font-size: 14px;
  }

  .data-points-data {
    font-size: 12px;
  }

  .dateFilter {

  }

  .select-label {
    font-size: 16px;
    font-family: 'Avenir';
  }

  .cancel-btn {
    background: none;
    color: black;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';

  }

  .ok-btn {
    background: none;
    color: black;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';

  }

  .report_pdf {
    background: none;
    color: black;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';
  }

  .cancel-btn:focus,
  .cancel-btn.focus {
    background-color: grey;
    border-color: #FFFFFF;
    color: #FFFFFF;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';
  }

  .cancel-btn:hover {
    background-color: grey;
    border-color: #FFFFFF;
    color: #FFFFFF;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';
  }

  .ok-btn:focus,
  .ok-btn.focus {
    background-color: #ff542c;
    border-color: #FFFFFF;
    color: #FFFFFF;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';
  }

  .ok-btn:hover {
    background-color: #ff542c;
    border-color: #FFFFFF;
    color: #FFFFFF;
    padding: 3px 12px;
    font-size: 14px;
    border-radius: 15px;
    font-family: 'Avenir';
  }

  #pgb {
    border-top: 2px solid black;
    padding-top: 12px;
    padding-bottom: 12px;
  }

  .orchy-btn-hover:hover {
    position: relative;
    display: inline-block;
    color: #FFFFFF;
    background-color: #ff542c;
    font-family: 'Avenir';
    font-size: 14px;
    cursor: pointer;
  }

</style>

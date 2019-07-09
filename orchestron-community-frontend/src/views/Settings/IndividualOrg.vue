<template>
    <div>
        <b-container fluid>
          <loading :active.sync="reloadPage" :can-cancel="true" :is-full-page="true"></loading>
            <settings-org-header :settingsHeader="headerData" :logoOrg="orgLogo" @updateOrg="updateOrg"></settings-org-header>
            <br>
            <b-container fluid style="background-color: #FFFFFF;" >
                <br>
                <p class="title">Bug Tracking System</p>
                <hr>
                <b-tabs style="background-color: #FFFFFF;">
                    <br>
                    <b-tab title="Bug Tracking System (  JIRA )" small >
                        <div >
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">URL:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="jiraURL"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter JIRA URL" :state="!$v.jiraURL.$invalid"></b-form-input>
                                          <p v-if="error_jira_msgs['jiraurl']" style="text-align: left;" class="error"> * {{ error_jira_msgs['jiraurl_msg']
                  }}</p>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">UserName:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="jiraUserName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter JIRA UserName" :state="!$v.jiraUserName.$invalid"></b-form-input>
                                        <p v-if="error_jira_msgs['jirauser']" style="text-align: left;" class="error"> * {{ error_jira_msgs['jirauser_msg']
                  }}</p>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Password:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="jiraPassword"
                                        type="password"
                                        class="inline-form-control"
                                        placeholder="Enter JIRA Password" :state="!$v.jiraPassword.$invalid"></b-form-input>
                                          <p v-if="error_jira_msgs['jirapwd']" style="text-align: left;" class="error"> * {{ error_jira_msgs['jirapwd_msg']
                  }}</p>
                                </b-col>
                            </b-row>
                          <p v-if="error_jira_msgs['invalid']" style="text-align: left;" class="error"> * {{ error_jira_msgs['invalid_msg'] }}</p>
                            <b-col cols="12" slot="modal-footer">
                                <br>
                                <div class="pull-right" style="float: right">
                                    <button type="button"
                                    class="btn btn-orange-close pull-right"
                                    @click=" testJiraConnection() " v-if="!$v.jiraURL.$invalid && !$v.jiraUserName.$invalid && !$v.jiraPassword.$invalid || jiraTestStatus!=='Success'"> Test Connection</button>
                                    <button type="button"
                                        class="btn btn-orange-submit pull-right"
                                        @click=" submitJiraConfig() " v-if="jiraTestStatus==='Success'">
                                    Submit
                                    </button>
                                </div>
                            </b-col>
                        </div>
                        <br>
                    </b-tab>
                    <b-modal
                                ref="updateOrgModal"
                                title="Update Organization"
                                size="lg"
                                centered>
                                <div>
                                    <form @submit.prevent="submitUpdateOrganization">
                                        <b-row class="my-1">
                                          <b-col cols="6">
                                            <b-col><label class="label">Name:</label></b-col>
                                            <b-col sm="12">
                                                <b-form-input
                                                    v-model="updateOrgName"
                                                    type="text"
                                                    class="inline-form-control"></b-form-input>
                                                    <p v-if="error_msgs['orgname']" style="text-align: left;" class="error"> * {{ error_msgs['orgname_msg']
                  }}</p>
                                            </b-col>
                                            </b-col>
                                          <b-col cols="6">
                                            <b-col><label class="label">Logo:</label></b-col>
                                            <b-col sm="12">
                                                <b-form-file
                                                    v-model="updateOrgLogo"
                                                    placeholder="Choose a logo..."
                                                    accept="image/jpeg, image/png,image/jpg,"
                                                    :state="!$v.updateOrgLogo.$invalid"></b-form-file>
                                                    <p v-if="error_msgs['orglogo']" style="text-align: left;" class="error"> * {{ error_msgs['orglogo_msg']
                  }}</p>
                                                <br>
                                                <p>{{ updateOrgLogo.name }}</p>
                                            </b-col>
                                          </b-col>
                                        </b-row>
                                        <br>
                                      <b-row class="my-1">
                                          <b-col cols="6">
                                            <b-col><label class="label">Location:</label></b-col>
                                            <b-col sm="12">
                                                <b-form-input
                                                    v-model="updateOrgLocation"
                                                    type="text"
                                                    class="inline-form-control"
                                                    placeholder="Enter Location" :state="!$v.updateOrgLocation.$invalid"></b-form-input>
                                                    <p  v-if="error_msgs['orgloc']" style="text-align: left;" class="error"> * {{ error_msgs['orgloc_msg'] }}</p>
                                            </b-col>
                                            </b-col>
                                          <b-col cols="6">
                                            <b-col><label class="label">Subscription End Date:</label></b-col>
                                            <b-col sm="12">
                                                <date-picker
                                                  v-model="updateOrgEndDate"
                                                  format="yyyy-MM-dd"
                                                  lang="en" width="100%"
                                                  :not-before="today" :state="!$v.updateOrgEndDate.$invalid"></date-picker>
                                                  <p  v-if="error_msgs['orgend']" style="text-align: left;" class="error"> * {{ error_msgs['orgend_msg'] }}</p>
                                            </b-col>
                                          </b-col>
                                        </b-row>
                                        <br>
                                      <b-row class="my-1">
                                          <b-col cols="6">
                                            <b-col><label class="label">Organization Type:</label></b-col>
                                            <b-col sm="12">
                                                <v-select
                                                    :options="orgTypeOption"
                                                    v-model="updateOrgType"
                                                    label="label"
                                                    placeholder="Select Organization Type"
                                                    :state="!$v.updateOrgType.$invalid"></v-select>
                                                    <p  v-if="error_msgs['orgind']" style="text-align: left;" class="error"> * {{ error_msgs['orgind_msg'] }}</p>
                                            </b-col>
                                            </b-col>
                                          <b-col cols="6">
                                            <b-col><label class="label">Timezone:</label></b-col>
                                            <b-col sm="12">
                                                <v-select
                                                    :options="orgTimezoneOption"
                                                    v-model="updateOrgTimezone"
                                                    label="label"
                                                    placeholder="Select Timezone"
                                                    :state="!$v.updateOrgTimezone.$invalid"></v-select>
                                                    <p v-if="error_msgs['orgtime']" style="text-align: left;" class="error"> * {{ error_msgs['orgtime_msg']
                  }}</p>


                                            </b-col>
                                          </b-col>
                                        </b-row>
                                        <br>
                                        <br>
                                    </form>
                                </div>
                                <b-col cols="12" slot="modal-footer">
                                    <div class="pull-right" style="float: right">
                                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeUpdateOrganization() "> Close</button>
                                        <button type="button"
                                                class="btn btn-orange-submit pull-right"
                                                data-dismiss="modal"
                                                @click=" submitUpdateOrganization() ">
                                        Submit
                                        </button>
                                    </div>
                                </b-col>
                      </b-modal>
                </b-tabs>
                <br>
            </b-container>
        </b-container>
    </div>
</template>

<script>
import settingsOrgHeader from '../../components/Settings/Header'
import UserTable from '../../components/Settings/UserTable'
import { required, minLength, email, url } from 'vuelidate/lib/validators'
import DatePicker from 'vue2-datepicker'
import axios from '@/utils/auth'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.min.css'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'IndividualOrg',
  components: {
    settingsOrgHeader,
    UserTable,
    Loading,
    DatePicker
  },
  data() {
    return {
      isLoading: false,
      reloadPage: false,
      today: new Date(),
      headerData: [],
      userData: [],
      userId: '',
      firstName: '',
      lastName: '',
      isAdmin: true,
      email: '',
      updateFirstName: '',
      updateLastName: '',
      updateEmail: '',
      updateIsAdmin: true,
      selectedBugTracking: 'JIRA',
      listBugTracking: ['JIRA'],
      jiraURL: '',
      jiraUserName: '',
      jiraPassword: '',
      selectedSmtp: '',
      listSmtpTypes: ['SMTP with Password'],
      emailHost: '',
      emailPort: '',
      emailUser: '',
      emailPassword: '',
      emailFromEmail: '',
      emailDisplayName: '',
      emailTlsSsl: '',
      transportLayerOption: ['TLS', 'SSL'],
      showConfig: false,
      enableJira: false,
      enableEmail: false,
      isConfCreated: false,
      jiraTestStatus: '',
      orgLogo: '',
      post_jira_method: false,
      updateOrgLogo: '',
      updateOrgLocation: '',
      updateOrgType: '',
      updateOrgTimezone: '',
      updateOrgEndDate: '',
      updateOrgName: '',
      orgTypeOption: [],
      orgTimezoneOption: [],
      error_msgs: {
          'usrfirst': false,
          'usrfirst_msg': '',
          'usrlast': false,
          'usrlast_msg': '',
          'usremail': false,
          'usremail_msg': '',
          'usrteam': false,
          'usrteam_msg': '',
          'usradmin': false,
          'usradmin_msg': '',
          'team': false,
          'team_msg': '',
          'teamdesc': false,
          'teamdesc_msg': '',
          'orgname': false,
          'orgname_msg': '',
          'orgloc': false,
          'orgloc_msg': '',
          'orglogo': false,
          'orglogo_msg': '',
          'orgtime': false,
          'orgtime_msg': '',
          'orgind': false,
          'orgind_msg': '',
          'orgend': false,
          'orgend_msg': ''
        },
    error_jira_msgs: {
      'jiraurl': false,
      'jiraurl_msg':'',
      'jirauser': false,
      'jirauser_msg':'',
      'jirapwd':false,
      'jirapwd_msg':'',
      'invalid': false,
      'invalid_msg': ''
    },
    }
  },
  validations: {
    firstName: {
      required,
      minLength: minLength(1)
    },
    lastName: {
      required,
      minLength: minLength(1)
    },
    email: {
      required,
      email,
      minLength: minLength(1)
    },
    updateFirstName: {
      required,
      minLength: minLength(1)
    },
    updateLastName: {
      required,
      minLength: minLength(1)
    },
    updateEmail: {
      required,
      email,
      minLength: minLength(1)
    },
    jiraURL: {
      required,
      url,
      minLength: minLength(1)
    },
    jiraUserName: {
      required,
      minLength: minLength(1)
    },
    jiraPassword: {
      required,
      minLength: minLength(1)
    },
    emailHost: {
      required,
      minLength: minLength(1)
    },
    emailPort: {
      required,
      minLength: minLength(1)
    },
    emailUser: {
      required,
      minLength: minLength(1)
    },
    emailPassword: {
      required,
      minLength: minLength(1)
    },
    emailFromEmail: {
      required,
      email,
      minLength: minLength(1)
    },
    emailDisplayName: {
      required,
      minLength: minLength(1)
    },
    emailTlsSsl: {
      required,
      minLength: minLength(1)
    },
    emailWithoutHost: {
      required,
      minLength: minLength(1)
    },
    emailWithoutPort: {
      required,
      minLength: minLength(1)
    },
    emailWithoutFromEmail: {
      required,
      email,
      minLength: minLength(1)
    },
    emailWithoutDisplayName: {
      required,
      minLength: minLength(1)
    },
    updateOrgName: {
      required
      // minLength: minLength(1)
    },
    updateOrgLogo: {
      
    },
    updateOrgLocation: {
      required
    },
    updateOrgEndDate: {
      required
    },
    updateOrgType: {
      required
    },
    updateOrgTimezone: {
      required
    }
  },
  created() {
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
    this.fetchData()
  },
   watch: {
      'updateOrgName': function (value_name) {
        if (value_name.length > 200) {
          this.error_msgs['orgname'] = true
          this.error_msgs['orgname_msg'] = 'Ensure this field has no more than 200 characters.'
        } else {
          this.error_msgs['orgname'] = false
        }
      },
      'updateOrgLogo': function (value_name) {
        this.error_msgs['orglogo'] = false
      },
      'updateOrgTimezone': function (value_name) {
        this.error_msgs['orgtime'] = false
      },
      'updateOrgLocation': function (value_name) {
        if (value_name.length > 100) {
          this.error_msgs['orgloc'] = true
          this.error_msgs['orgloc_msg'] = 'Ensure this field has no more than 100 characters.'
        } else {
          this.error_msgs['orgloc'] = false
        }
      },
      'updateOrgType': function (value_name) {
        this.error_msgs['orgind'] = false
      },
      'firstName': function (value_name) {
        if (value_name.length > 30) {
          this.error_msgs['usrfirst'] = true
          this.error_msgs['usrfirst_msg'] = 'Ensure this field has no more than 30 characters.'
        } else {
          this.error_msgs['usrfirst'] = false
        }
      },
      'lastName': function (value_name) {
        if (value_name.length > 30) {
          this.error_msgs['usrlast'] = true
          this.error_msgs['usrlast_msg'] = 'Ensure this field has no more than 30 characters.'
        } else {
          this.error_msgs['usrlast'] = false
        }
      },
      'jiraURL': function (value_name) {
        this.error_msgs['jiraurl'] = false
      },
      'jiraUserName': function (value_name) {
        this.error_msgs['jirauser'] = false
      },

      'jiraPassword': function (value_name) {
        this.error_msgs['jirapwd'] = false
      },



    },
  updated() {
    this.$nextTick(function() {     
      if (this.isLoading) {
        this.headerData = []
        this.userData = []
        this.fetchData()
        this.isLoading = false
        this.reloadPage = false
      }
    })
  },
  methods: {
    closeUpdateOrganization() {
      this.$refs.updateOrgModal.hide()
    },
    fetchData() {       
      if (this.org && this.token) {
         this.reloadPage = true
        axios
          .get('/organizations/' + this.org + '/')
          .then(res => {
            let isAdmin
            this.headerData.push({
              logo: res.data.logo,
              name: res.data.name,
              timezone: res.data.timezone,
              location: res.data.location,
              endDate: res.data.end_date
            })
            axios.get(res.data.logo)
              .then(res => {
                this.orgLogo = res.data
              })
          })
          .catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
                notValidUser()
                this.$router.push('/')
            }
            if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })

        axios
        .get('/organizations/' + this.org + '/jira/')
        .then(res => {
          this.jiraURL = res.data.url
          this.jiraUserName = '****'
          this.jiraPassword = ''
          this.post_jira_method = true
        }).catch(error => {
          if (error.response.data.detail === 'Signature has expired.'){
                notValidUser()
                this.$router.push('/')
            }
            this.post_jira_method = false
          })
        this.reloadPage = false


    axios.get('/organizations/options/')
            .then(res => {
              for (const value of res.data.timezone) {
                this.orgTimezoneOption.push(value[1])
              }
              for (const value of res.data.industry) {
                this.orgTypeOption.push({ value: value[0], label: value[1] })
              }
                this.reloadPage = false
              
            }).catch(error => {
              if (error.response.data.detail === 'Signature has expired.'){
                notValidUser()
                this.$router.push('/')
              } 
                this.reloadPage = false

              if (error.response.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.response.status === 403) {
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
    updateOrg(){
        if (this.org && this.token) {
            this.updateOrgId = this.org
            this.orgId = this.org
            axios.get('/organizations/'+this.org+'/')
              .then(res => {;
                this.updateOrgName = res.data.name
                this.updateOrgLocation = res.data.location
                // this.updateOrgType = res.data.industry
                this.updateOrgTimezone = res.data.timezone
                this.updateOrgEndDate = res.data.end_date
                for (const appVal of this.orgTypeOption) {
                  if (res.data.industry === appVal.value) {
                    this.updateOrgType = {'label':appVal.label, 'value':res.data.industry}
                  }
                }
                this.$refs.updateOrgModal.show()
              }).catch(error => {
                if (error.response.data.detail === 'Signature has expired.'){
                notValidUser()
                this.$router.push('/')
              }
                if (error.response.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.response.status === 403) {
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
     submitUpdateOrganization() {
          if (this.org && this.token) {
            const orgEndDate = new Date(this.updateOrgEndDate)
            const d = orgEndDate.getDate()
            const m = orgEndDate.getMonth() + 1
            const y = orgEndDate.getFullYear()
            const endDate = y + '-' + (m <= 9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d)
            const form_data = new FormData()
              if (this.updateOrgLogo) {
              form_data.append('logo', this.updateOrgLogo)
            }
            form_data.append('name', this.updateOrgName)
            // form_data.append('logo', this.updateOrgLogo)
            form_data.append('location', this.updateOrgLocation)
            form_data.append('industry', this.updateOrgType.value)
            form_data.append('timezone', this.updateOrgTimezone)
            form_data.append('end_date', endDate)
            axios.post('/organizations/' + this.orgId + '/', form_data, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
              .then(res => {
                this.$refs.updateOrgModal.hide()
                this.isLoading = true
                // this.$router.push('/settings/')
                this.updateOrgId = ''
                this.$notify({
                  group: 'foo',
                  type: 'info',
                  title: 'success',
                  text: 'The organization has been updated successfully!',
                  position: 'top right'
                })
                this.reloadPage = true
              }).catch(error => {
                if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
                }
                if (error.response.status === 404) {
                  this.$router.push('/not_found')
                }

                if (error.response.status === 400) {
                if (error.response.data['name']) {
                  this.error_msgs['orgname'] = true
                  this.error_msgs['orgname_msg'] = error.response.data['name'][0]
                }
                if (error.response.data['timezone']) {
                  this.error_msgs['orgtime'] = true
                  this.error_msgs['orgtime_msg'] = error.response.data['timezone'][0]
                }
                if (error.response.data['end_date']) {
                  this.error_msgs['orgend'] = true
                  this.error_msgs['orgend_msg'] = error.response.data['end_date'][0]
                }
                if (error.response.data['location']) {
                  this.error_msgs['orgloc'] = true
                  this.error_msgs['orgloc_msg'] = error.response.data['location'][0]
                }
                if (error.response.data['industry']) {
                  this.error_msgs['orgind'] = true
                  this.error_msgs['orgind_msg'] = error.response.data['industry'][0]
                }
                if (error.response.data['logo']) {
                  this.error_msgs['orglogo'] = true
                  this.error_msgs['orglogo_msg'] = error.response.data['logo'][0]
                }
              }

                else {
                  this.$router.push('/error')
                }
              })
          }else {
            notValidUser()
            this.$router.push('/')
          }
        },
    testJiraConnection() {
      if (this.org && this.org && this.token) {
        this.isLoading = true
        const form_data = {
          url: this.jiraURL,
          username: this.jiraUserName,
          password: this.jiraPassword
        }
        axios
          .post('/jira/connection/test/', form_data)
          .then(res => {
            this.jiraTestStatus = res.data.status
            this.isLoading = false
          })
          .catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
            }
            if (error.response.status === 400) {
              if (error.response.data['url']) {
                this.error_jira_msgs['jiraurl'] = true
                this.error_jira_msgs['jiraurl_msg'] = error.response.data['url'][0]
              }
              if (error.response.data['username']) {
                this.error_jira_msgs['jirauser'] = true
                this.error_jira_msgs['jirauser_msg'] = error.response.data['username'][0]
              }
              if (error.response.data['password']) {
                this.error_jira_msgs['jirapwd'] = true
                this.error_jira_msgs['jirapwd_msg'] = error.response.data['password'][0]
              }
              
            }
            else{
              this.error_jira_msgs['invalid'] = true
              this.error_jira_msgs['invalid_msg'] = "Provided credentials are invalid or server timeout"

            }

            // this.$notify({
            //   group: 'foo',
            //   type: 'error',
            //   title: 'error',
            //   text: 'Please enter a valid JIRA credentials',
            //   position: 'top right'
            // })
            this.isLoading = false
          })
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    submitJiraConfig() {
      if (this.org && this.token) {
        const form_data = {
          url: this.jiraURL,
          username: this.jiraUserName,
          password: this.jiraPassword
        }
        if(this.post_jira_method){
        axios
          .post('/organizations/' + this.org + '/jira/', form_data)
          .then(res => {
          
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.org + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The JIRA configuration has been updated successfully!',
                position: 'top right'
              })
              this.isLoading = false
          })
          .catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
            }
            if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
        }
        else{
             axios
          .put('/organizations/' + this.org + '/jira/', form_data)
          .then(res => {
            
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.org + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The JIRA configuration has been created successfully!',
                position: 'top right'
              })
              this.isLoading = false
          })
          .catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
            }
            if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
        }
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    submitWithPasswordSMTP() {
      if (this.org && this.org && this.token) {
        const form_data = new FormData()
        form_data.append('host', this.emailHost)
        form_data.append('username', this.emailUser)
        form_data.append('password', this.emailPassword)
        form_data.append('port', this.emailPort)
        form_data.append('from_email', this.emailFromEmail)
        form_data.append('display_name', this.emailDisplayName)
        form_data.append('certs', this.emailTlsSsl)
        axios
          .put('/organizations/' + this.org + '/email/', form_data)
          .then(res => {
              this.$refs.userCreateModal.hide()
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.org + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The email configuration has been created successfully!',
                position: 'top right'
              })
              this.isLoading = false
          })
          .catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
            }
            if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 404) {
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
  .title {
    font-family: "Avenir";
    font-size: 14px;
    line-height: 1.33;
    color: #000000;
  }

  .btn-orange-close {
    color: #ff542c;
    background-color: #ffffff;
    border-color: #ff542c;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-close:focus,
  .btn-orange-close.focus {
    color: #ff542c;
    background-color: #ffffff;
    border-color: #ff542c;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-close:hover {
    color: #ffffff;
    background-color: #ff542c;
    border-color: #ffffff;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit {
    color: #ffffff;
    background-color: #ff542c;
    border-color: #ffffff;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit:focus,
  .btn-orange-submit.focus {
    color: #ffffff;
    background-color: #ff542c;
    border-color: #ffffff;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit:hover {
    color: #ffffff;
    background-color: #ff542c;
    border-color: #ffffff;
    font-family: "Avenir";
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }
  .error {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 400;
    line-height: 0.99;
    text-align: center;
    color: #f44336;
  }
</style>

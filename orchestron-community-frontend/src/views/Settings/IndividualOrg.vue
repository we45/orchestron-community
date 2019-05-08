<template>
    <div>
        <b-container fluid>
          <loading :active.sync="reloadPage" :can-cancel="true" :is-full-page="true"></loading>
            <settings-org-header :settingsHeader="headerData" :logoOrg="orgLogo" @configureSettings="configureOrgSettings"></settings-org-header>
            <b-container fluid v-if="showConfig" style="background-color: #FFFFFF;">
                <br>
                <p>Organization Configure</p>
                <hr>
                <b-row>
                    <b-col cols="1"></b-col>
                    <b-col cols="10">
                        <b-row>
                            <b-col cols="6">
                                <b-row>
                                    <b-col sm="6"><label class="label">Enable JIRA:</label></b-col>
                                    <b-col sm="6">
                                        <toggle-button
                                            v-model="enableJira"
                                            :value="enableJira" :labels="{checked: 'Yes', unchecked: 'No'}" :width="60" :height="30" style="font-size: 12px;"/>
                                    </b-col>
                                </b-row>
                            </b-col>
                            <b-col cols="6">
                            <b-row>
                                    <b-col sm="6"><label class="label">Enable Email:</label></b-col>
                                    <b-col sm="6">
                                        <toggle-button
                                            v-model="enableEmail"
                                            :value="enableEmail" :labels="{checked: 'Yes', unchecked: 'No'}" :width="60" :height="30" style="font-size: 12px;"/>
                                    </b-col>
                                </b-row>
                            </b-col>

                          <b-col>
                            <br>
                            <div class="pull-right" style="float: right">
                                <button type="button"
                                    class="btn btn-orange-submit pull-right"
                                    @click=" submitOrgConfigSettings() ">
                                Submit
                                </button>
                            </div>
                            </b-col>
                        </b-row>
                        <br>
                    </b-col>
                    <b-col cols="1"></b-col>
                </b-row>
            </b-container>
            <br>
            <b-container fluid style="background-color: #FFFFFF;">
                <br>
                <p class="title">Manage Users</p>
                <hr>
                <b-tabs style="background-color: #FFFFFF;">
                    <br>
                    <b-tab title="Users" small>
                        <div>
                            <br>
                            <b-container fluid>
                                <user-table
                                :data-items="userData"
                                @updateModal="updateUser($event)"
                                @deleteModal="deleteUser($event)"
                                @createModal="createUser"></user-table>
                            </b-container>
                        </div>
                    </b-tab>
                </b-tabs>
                <br>
                <!--User Create-->
                <b-modal
                    ref="userCreateModal"
                    title="Create User"
                    size="lg"
                    centered>
                    <div>
                        <form @submit.prevent="submitCreateUser">
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">First Name:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="firstName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter First Name" :state="!$v.firstName.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Last Name:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="lastName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Last Name" :state="!$v.lastName.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Email:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="email"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Email" :state="!$v.email.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                        </form>
                    </div>
                    <b-col cols="12" slot="modal-footer">
                        <div class="pull-right" style="float: right">
                            <button type="button" class="btn btn-orange-close pull-right" @click=" closeCreateUser() "> Close</button>
                            <button type="button" class="btn btn-orange-submit pull-right"
                                data-dismiss="modal"
                                @click=" submitCreateUser() "
                                v-if="!$v.firstName.$invalid && !$v.lastName.$invalid && !$v.email.$invalid">
                            Submit
                            </button>
                        </div>
                    </b-col>
                </b-modal>
                <!--UserUpdate-->
                <b-modal
                    ref="userUpdateModal"
                    title="Update User"
                    size="lg"
                    centered>
                    <div>
                        <form @submit.prevent="submitUpdateUser">
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">First Name:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="updateFirstName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter First Name" :state="!$v.updateFirstName.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Last Name:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="updateLastName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Last Name" :state="!$v.updateLastName.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Email:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="updateEmail"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Email" :state="!$v.updateEmail.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                        </form>
                    </div>
                    <b-col cols="12" slot="modal-footer">
                        <div class="pull-right" style="float: right">
                            <button type="button" class="btn btn-orange-close pull-right" @click=" closeUpdateUser() "> Close</button>
                            <button type="button" class="btn btn-orange-submit pull-right"
                                data-dismiss="modal"
                                @click=" submitUpdateUser() "
                                v-if="!$v.updateFirstName.$invalid && !$v.updateLastName.$invalid && !$v.updateEmail.$invalid">
                            Submit
                            </button>
                        </div>
                    </b-col>
                </b-modal>
                <!--Delete User-->
                <b-modal ref="deleteUserModal" title="Delete User" centered size="lg">
                    <div>
                        <form @submit.prevent="deleteSubmitUser">
                            <p class="delete-header">Are you sure want to delete this User ?</p>
                            <br>
                            <br>
                        </form>
                    </div>
                    <b-col cols="12" slot="modal-footer">
                        <div class="pull-right" style="float: right;">
                            <button type="button" class="btn btn-orange-close" @click=" deleteCloseSubmitUser() ">No</button>
                            <button type="button" class="btn btn-orange-submit"
                                data-dismiss="modal" @click=" deleteSubmitUser() ">
                            Yes
                            </button>
                        </div>
                    </b-col>
                </b-modal>
            </b-container>
            <br>
            <b-container fluid style="background-color: #FFFFFF;" v-if="enableJira || enableEmail">
                <br>
                <p class="title">Manage Communication and Bug Tracking System</p>
                <hr>
                <b-tabs style="background-color: #FFFFFF;">
                    <br>
                    <b-tab title="Bug Tracking System" small v-if="enableJira">
                        <b-row>
                            <b-col cols="12">
                                <b-col cols="4">
                                    <label>Select Bug Tracking System:</label>
                                </b-col>
                                <b-col cols="8">
                                    <v-select
                                        v-model="selectedBugTracking"
                                        :options="listBugTracking"
                                        placeholder="Select Bug Tracking System" ></v-select>
                                </b-col>
                            </b-col>
                        </b-row>
                        <br>
                        <br>
                        <div v-if="selectedBugTracking==='JIRA' && enableJira">
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">URL:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="jiraURL"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter JIRA URL" :state="!$v.jiraURL.$invalid"></b-form-input>
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
                                </b-col>
                            </b-row>
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
                    <b-tab title="Email" small v-if="enableEmail">
                        <b-row>
                            <b-col cols="12">
                                <b-col cols="4">
                                    <label>Select SMTP Type:</label>
                                </b-col>
                                <b-col cols="8">
                                    <v-select
                                        v-model="selectedSmtp"
                                        :options="listSmtpTypes"
                                        placeholder="Select SMTP Type" ></v-select>
                                </b-col>
                            </b-col>
                        </b-row>
                        <br>
                        <br>
                        <div v-if="selectedSmtp==='SMTP with Password' && enableEmail">
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">HOST:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailHost"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Email Host" :state="!$v.emailHost.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Port:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailPort"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Email Port" :state="!$v.emailPort.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Host User:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailUser"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Host User" :state="!$v.emailUser.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Password:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailPassword"
                                        type="password"
                                        class="inline-form-control"
                                        placeholder="Enter Password" :state="!$v.emailPassword.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">From Email:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailFromEmail"
                                        type="email"
                                        class="inline-form-control"
                                        placeholder="Enter From Email" :state="!$v.emailFromEmail.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Display Name:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="emailDisplayName"
                                        type="text"
                                        class="inline-form-control"
                                        placeholder="Enter Display Name" :state="!$v.emailDisplayName.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">TLS/SSL:</label></b-col>
                                <b-col sm="10">
                                    <v-select v-model="emailTlsSsl" :options="transportLayerOption" placeholder="Select Transport Layer" :state="!$v.emailTlsSsl.$invalid"></v-select>
                                </b-col>
                            </b-row>
                            <b-col cols="12">
                                <div class="pull-right" style="float: right">
                                    <button type="button"
                                        class="btn btn-orange-close pull-right"
                                        @click=" submitWithPasswordSMTP() "
                                        v-if="!$v.emailHost.$invalid && !$v.emailPort.$invalid && !$v.emailUser.$invalid
                                        && !$v.emailPassword.$invalid && !$v.emailFromEmail.$invalid && !$v.emailDisplayName.$invalid
                                        && !$v.emailTlsSsl.$invalid">Save Configuration</button>
                                </div>
                            </b-col>
                        </div>
                    </b-tab>
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
import axios from '@/utils/auth'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.min.css'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'IndividualOrg',
  components: {
    settingsOrgHeader,
    UserTable,
    Loading
  },
  data() {
    return {
      isLoading: false,
      reloadPage: false,
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
      post_jira_method: false
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
    }
  },
  created() {
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
    this.param = this.$route.params.orgId
    this.fetchData()
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
    fetchData() {
        this.reloadPage = true
      if (this.param && this.org && this.token) {
        axios
          .get('/organizations/' + this.param + '/?users=1&groups=1')
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
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 403) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })
            for (const value of res.data.users) {
              let name = ''
              if (
                value.fields.first_name == null ||
              value.fields.last_name === null
              ) {
                name = value.fields.email
              } else if (
                value.fields.first_name === null &&
              value.fields.last_name == null
              ) {
                name = value.fields.email
              } else {
                name = value.fields.first_name + ' ' + value.fields.last_name
              }
              if (value.fields.is_admin === true) {
                isAdmin = true
              }
              this.userData.push({
                name: name,
                email: value.fields.email,
                id: value.fields.id,
                isAdmin: isAdmin
              })
            }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })

        axios
          .get('/organizations/' + this.param + '/config/')
          .then(res => {
            this.enableJira = res.data.enable_jira
            this.enableEmail = res.data.enable_email
            this.isConfCreated = true
            if (this.enableJira) {
              axios
                .get('/organizations/' + this.param + '/jira/')
                .then(res => {
                  this.jiraURL = res.data.url
                  this.jiraUserName = '****'
                  this.jiraPassword = ''
                  this.post_jira_method = true
                })
                .catch(error => {
        this.reloadPage = false

          

                  if (error.res.status === 404) {
                    this.$router.push('/not_found')
                  } else if (error.res.status === 403) {
                    this.$router.push('/forbidden')
                  } else {
                    this.$router.push('/error')
                  }
                })
            }
            this.reloadPage = false
          })
          .catch(error => {
        this.reloadPage = false

            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
        // this.reloadPage = false

      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    createUser() {
      this.$refs.userCreateModal.show()
    },
    closeCreateUser() {
      this.$refs.userCreateModal.hide()
    },
    submitCreateUser() {
      if (this.param && this.org && this.token) {
        const form_data = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          is_staff: true,
          org: this.param,
          is_admin: this.isAdmin
        }
        axios
          .put('/users/', form_data)
          .then(res => {
            if (res.status === 200) {
              this.$refs.userCreateModal.hide()
              this.isLoading = true
              this.reloadPage = true
              this.$router.push('/settings/individual_org/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'User',
                text: 'The user has been created Successfully!',
                position: 'top right'
              })
            }
          })
          .catch(error => {
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
    updateUser(event) {
      this.userId = event.id
      this.$refs.userUpdateModal.show()
      if (this.param && this.org && this.token) {
        axios
          .get('/users/' + this.userId + '/')
          .then(res => {
            if (res.status === 200) {
              this.updateFirstName = res.data.first_name
              this.updateLastName = res.data.last_name
              this.updateEmail = res.data.email
              this.updateIsAdmin = res.data.is_admin
            }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 404) {
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
    closeUpdateUser() {
      this.$refs.userUpdateModal.hide()
    },
    submitUpdateUser() {
      const form_data = {
        first_name: this.updateFirstName,
        last_name: this.updateLastName,
        email: this.updateEmail,
        is_staff: true,
        org: this.param,
        is_admin: this.updateIsAdmin
      }
      if (this.param && this.org && this.token) {
        axios
          .post('/users/' + this.userId + '/', form_data)
          .then(res => {
            if (res.status === 200) {
              this.$refs.userUpdateModal.hide()
              this.isLoading = true
              this.$router.push('/settings/individual_org/' + this.param + '/')
              this.userId = ''
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'User',
                text: 'The user has been updated Successfully!',
                position: 'top right'
              })
            }
          })
          .catch(error => {
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
    deleteUser(event) {
      this.userId = event.id
      this.$refs.deleteUserModal.show()
    },
    deleteCloseSubmitUser() {
      this.$refs.deleteUserModal.hide()
    },
    deleteSubmitUser() {
      if (this.param && this.userId && this.org && this.token) {
        axios
          .delete('/users/' + this.userId + '/')
          .then(res => {
            if (res.status === 200) {
              this.$refs.deleteUserModal.hide()
              this.userId = ''
              this.isLoading = true
              this.$router.push('/settings/individual_org/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'User',
                text: 'The user has been deleted Successfully!',
                position: 'top right'
              })
            }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 404) {
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
    configureOrgSettings() {
      if (this.showConfig === true) {
        this.showConfig = false
      } else {
        this.showConfig = true
      }
    },
    submitOrgConfigSettings() {
      const form_data = {
        'enable_jira': this.enableJira,
        'enable_email': this.enableEmail
      }
      if (this.param && this.org && this.token) {
        if (this.isConfCreated) {
          axios
            .post('/organizations/' + this.param + '/config/', form_data)
            .then(res => {
              if (res.status === 200) {
                this.showConfig = false
                this.isLoading = true
                this.$router.go('/settings/individual_org/' + this.param + '/')
                this.$notify({
                  group: 'foo',
                  type: 'success',
                  title: 'Organization Configuration',
                  text: 'The Organization has been created Successfully!',
                  position: 'top right'
                })
              }
            })
            .catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        } else {
          axios
            .put('/organizations/' + this.param + '/config/', form_data)
            .then(res => {
              if (res.status === 200) {
                this.showConfig = false
                this.isLoading = true
                this.$router.go('/settings/individual_org/' + this.param + '/')
                this.$notify({
                  group: 'foo',
                  type: 'success',
                  title: 'Organization Configuration',
                  text: 'The Organization has been created Successfully!',
                  position: 'top right'
                })
              }
            })
            .catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
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
    testJiraConnection() {
      if (this.param && this.org && this.token) {
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
            this.$notify({
              group: 'foo',
              type: 'error',
              title: 'JIRA',
              text: 'Please enter a valid JIRA Credentials',
              position: 'top right'
            })
            this.isLoading = false
          })
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    submitJiraConfig() {
      if (this.param && this.org && this.token) {
        const form_data = {
          url: this.jiraURL,
          username: this.jiraUserName,
          password: this.jiraPassword
        }
        if(this.post_jira_method){

        axios
          .post('/organizations/' + this.param + '/jira/', form_data)
          .then(res => {
            // if (res.status === 200) {
              this.$refs.userCreateModal.hide()
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'JIRA',
                text: 'The JIRA has been updated Successfully!',
                position: 'top right'
              })
              this.isLoading = false
            // }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
        }
        else{
             axios
          .put('/organizations/' + this.param + '/jira/', form_data)
          .then(res => {
            // if (res.status === 200) {
              this.$refs.userCreateModal.hide()
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'JIRA',
                text: 'The JIRA has been created Successfully!',
                position: 'top right'
              })
              this.isLoading = false
            // }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
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
      if (this.param && this.org && this.token) {
        const form_data = new FormData()
        form_data.append('host', this.emailHost)
        form_data.append('username', this.emailUser)
        form_data.append('password', this.emailPassword)
        form_data.append('port', this.emailPort)
        form_data.append('from_email', this.emailFromEmail)
        form_data.append('display_name', this.emailDisplayName)
        form_data.append('certs', this.emailTlsSsl)
        axios
          .put('/organizations/' + this.param + '/email/', form_data)
          .then(res => {
            if (res.status === 200) {
              this.$refs.userCreateModal.hide()
              this.isLoading = true
              this.$router.go('/settings/individual_org/' + this.param + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Email',
                text: 'The Email has been created Successfully!',
                position: 'top right'
              })
              this.isLoading = false
            }
          })
          .catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 404) {
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
</style>

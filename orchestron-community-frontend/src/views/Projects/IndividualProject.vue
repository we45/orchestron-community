<template>
    <div>
        <b-container fluid>
            <loading :active.sync="reloadPage" :can-cancel="true"></loading>
            <headers :name="projectName" :createdOn="projectCreatedOn" :logo="projectLogo"></headers>
            <br>
            <common-table
              :pageCount="applicationCount"
              :dataItems="vulnerabilitiesList"
              :headerTitle="headerTitles"
              @createModal="createApplication"
              @updateModal="updateApplication($event)"
              @clickPagination="clickProjPagination($event)"
              @deleteModal="beforeDeleteModal($event)"></common-table>
            <b-modal ref="createApplicationModal" title="Create Application" centered size="lg">
                <div>
                    <form @submit.prevent="submitCreateApplication">
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Name: *</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appName"
                                      type="text"
                                      class="inline-form-control"
                                      :state="!$v.appName.$invalid"
                                      placeholder="Create Application Name">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                            <b-col cols="6">
                                <label class="label">Logo:</label>
                                <b-col sm="12">
                                    <b-form-file
                                      ref="fileinput"
                                      v-model="appLogo"
                                      accept="image/jpeg, image/png,image/jpg,"
                                      :state="!$v.appLogo.$invalid"
                                      placeholder="Choose a logo..."></b-form-file>
                                  <br>
                                  <p>{{ appLogo.name }}</p>
                                </b-col>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Target Type: *</label>
                                <b-col sm="12">
                                  <v-select
                                    :options="appTargetOption"
                                    v-model="appHostType"
                                    placeholder="Select Target Type"
                                    :state="!$v.appHostType.$invalid"></v-select>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">Platform Type: *</label>
                              <b-col sm="12">
                                <v-select
                                  :options="appPlatformOption"
                                  v-model="appPlatformTags"
                                  placeholder="Select Platform"
                                  :state="!$v.appPlatformTags.$invalid"></v-select>
                              </b-col>
                          </b-col>

                        </b-row>
                        <br>
                      <b-row class="my-1">
                          <b-col cols="6">
                                <label class="label">URL: *</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appUrl"
                                      type="text"
                                      :state="!$v.appUrl.$invalid"
                                      class="inline-form-control"
                                      placeholder="http://example.com">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">IPv4: *</label>
                              <b-col sm="12">
                                  <b-form-input
                                    v-model="appIpv4"
                                    :state="!$v.appIpv4.$invalid"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="127.0.0.1">
                                  </b-form-input>
                              </b-col>
                          </b-col>
                      </b-row>
                      <br>
                      <b-row class="my-1">
                          <b-col cols="6">
                              <label class="label">OS Info: *</label>
                              <b-col sm="12">
                                <b-form-input
                                  v-model="appOsInfo"
                                  type="text"
                                  class="inline-form-control"
                                  :state="!$v.appOsInfo.$invalid"
                                  placeholder="Ubuntu">
                                </b-form-input>
                              </b-col>
                          </b-col>
                      </b-row>
                      <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeCreateApplication() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitCreateApplication() "
                                v-if="!$v.appName.$invalid && !$v.appLogo.$invalid && !$v.appHostType.$invalid
                            && !$v.appPlatformTags.$invalid && !$v.appIpv4.$invalid && !$v.appOsInfo.$invalid && !$v.appUrl.$invalid" :disabled="isClicked">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Update Modal-->
            <b-modal ref="updateApplicationModal" title="Update Application" centered size="lg">
                <div>
                    <form @submit.prevent="submitUpdateApplication">
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Name: *</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appUpdateName"
                                      type="text"
                                      class="inline-form-control"
                                      :state="!$v.appUpdateName.$invalid"
                                      placeholder="Update Application Name">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                            <b-col cols="6">
                                <label class="label">Logo:</label>
                                <b-col sm="12">
                                    <b-form-file
                                      v-model="appUpdateLogo"
                                      placeholder="Choose a logo..."
                                      accept="image/jpeg, image/png,image/jpg,"></b-form-file>
                                  <br>
                                  <p>{{ appUpdateOldLogoName }}</p>
                                </b-col>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Target Type: *</label>
                                <b-col sm="12">
                                  <v-select
                                    :options="appTargetOption"
                                    v-model="appUpdateHostType"
                                    :state="!$v.appUpdateHostType.$invalid"></v-select>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">Platform Type: *</label>
                              <b-col sm="12">
                                <v-select
                                  :options="appPlatformOption"
                                  v-model="appUpdatePlatformTags"
                                  :state="!$v.appUpdatePlatformTags.$invalid"></v-select>
                              </b-col>
                          </b-col>

                        </b-row>
                        <br>
                      <b-row class="my-1">
                          <b-col cols="6">
                                <label class="label">URL: *</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appUpdateUrl"
                                      type="text"
                                      :state="!$v.appUpdateUrl.$invalid"
                                      class="inline-form-control"
                                      placeholder="http://example.com">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">IPv4: *</label>
                              <b-col sm="12">
                                  <b-form-input
                                    v-model="appUpdateIpv4"
                                    type="text"
                                    class="inline-form-control"
                                    :state="!$v.appUpdateIpv4.$invalid"
                                    placeholder="127.0.0.1">
                                  </b-form-input>
                              </b-col>
                          </b-col>
                      </b-row>
                      <br>
                      <b-row class="my-1">
                          <b-col cols="6">
                              <label class="label">OS Info: *</label>
                              <b-col sm="12">
                                <b-form-input
                                  v-model="appUpdateOsInfo"
                                  type="text"
                                  class="inline-form-control"
                                  :state="!$v.appUpdateOsInfo.$invalid"
                                  placeholder="Ubuntu">
                                </b-form-input>
                              </b-col>
                          </b-col>
                      </b-row>
                      <br>
                    </form>
                </div>
              <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeUpdateApplication() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitUpdateApplication() "
                                v-if="!$v.appUpdateName.$invalid && !$v.appUpdateHostType.$invalid
                            && !$v.appUpdatePlatformTags.$invalid && !$v.appUpdateIpv4.$invalid
                            && !$v.appUpdateOsInfo.$invalid && !$v.appUpdateUrl.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Delete Modal-->
            <b-modal ref="beforedeleteApplicationModal" title="Delete Application" centered size="lg">
                <div>
                    <form @submit.prevent="BeforeSubmitDeleteApplication">
                        <p class="delete-header">Are you sure want to delete this application ?</p>
                        <br>
                        <p class="delete-sub">* Deleting this application will delete all Vulnerabilities associated with it</p>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" beforeCloseDeleteApplication() ">No</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" BeforeSubmitDeleteApplication() ">
                        Yes
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <b-modal ref="deleteApplicationModal" title="Delete Application" centered size="lg">
                <div>
                    <form @submit.prevent="submitDeleteApplication">
                        <input type="hidden" v-model="deleteApplicationId">
                        <p class="delete-header">Are you sure want to delete this application ?</p>
                        <br>
                        <b-form-input
                            v-model="typeDelete"
                            type="text"
                            class="inline-form-control"
                            placeholder="Type DELETE" ></b-form-input>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeDeleteApplication() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitDeleteApplication() " v-if="typeDelete==='DELETE'">
                        Delete
                        </button>
                    </div>
                </b-col>
            </b-modal>
        </b-container>
    </div>
</template>

<script>
  import CommonTable from '../../components/Projects/CommonTable'
  import Headers from '../../components/Projects/Headers'
  import axios from '@/utils/auth'
  import { required, minLength, url, ipAddress } from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import { notValidUser } from '@/utils/checkAuthUser'

  export default {
    name: 'IndividualProject',
    components: {
      CommonTable,
      Headers,
      Loading
    },
    data() {
      return {
        isLoading: false,
        vulnerabilitiesList: [],
        projectDetails: [],
        projectData: '',
        projectName: '',
        projectLogo: '',
        projectCreatedOn: '',
        projectId: '',
        headerTitles: 'List of Application',
        appName: '',
        appLogo: '',
        appHostType: '',
        appTargetOption: '',
        appUrl: '',
        appPlatformOption: '',
        appPlatformTags: '',
        appIpv4: '',
        appOsInfo: '',
        appUpdateName: '',
        appUpdateLogo: '',
        appUpdateHostType: '',
        appUpdateUrl: '',
        appUpdatePlatformTags: '',
        appUpdateIpv4: '',
        appUpdateOsInfo: '',
        appUpdateOldLogoName: '',
        updateApplicationId: '',
        deleteApplicationId: '',
        typeDelete: '',
        applicationCount: 0,
        reloadPage : false,
        paginatedVulnerabilitiesList: [],
        isClicked: false,

      }
    },
    validations: {
      appUrl:{
        required,
        url
      },
      appUpdateUrl:{
        required,
        url
      },
      appName: {
        required,
        minLength: minLength(1)
      },
      appLogo: {

      },
      appHostType: {
        required
      },
      appPlatformTags: {
        required
      },
      appIpv4: {
        required,
        ipAddress
      },
      appOsInfo: {
        required
      },
      appUpdateName: {
        required,
        minLength: minLength(1)
      },
      appUpdateHostType: {
        required
      },
      appUpdatePlatformTags: {
        required
      },
      appUpdateIpv4: {
        required,
        ipAddress
      },
      appUpdateOsInfo: {
        required
      }
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.param = this.$route.params.projectId
      this.fetchProjectData()
      this.fetchData()
    },
    // updated() {
    //   this.$nextTick(function() {
    //     if (this.isLoading) {
    //       this.vulnerabilitiesList = []
    //       this.fetchData()
    //       this.isLoading = false
    //     }
    //   })
    // },
    methods: {
      fetchProjectData() {
        if (this.param && this.org && this.token) {
          axios.get('/projects/' + this.param + '/?applications=1')
            .then(res => {
              this.projectName = res.data.name
              this.projectId = res.data.id
              axios.get(res.data.logo)
                .then(res => {
                  this.projectLogo = res.data
                }).catch(error => {
                  if (error.res.status === 404) {
                    this.$router.push('/not_found')
                  } else if (error.res.status === 403) {
                    this.$router.push('/forbidden')
                  } else {
                    this.$router.push('/error')
                  }
                })
              this.projectCreatedOn = res.data.created_on            
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
      fetchData() {
        this.reloadPage = true
        if (this.param && this.org && this.token) {
          axios.get('/projects/' + this.param + '/applications/?page=1')
            .then(res => {
              this.applicationCount = res.data.count
              this.vulnerabilitiesList = []
              for (const value of res.data.results) {
                this.vulnerabilitiesList.push({
                  name: { vul_name: value.name },
                  sev: value.stats.severity_count,
                  id: value.id,
                  url: '/projects/individual_application/' + value.id + '/'
                })
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
       clickProjPagination(event) {
        if (event.page) {
          if (event.page > 1) {
            axios.get('/projects/' + this.param + '/applications/?page=' + event.page)
              .then(res => {
                this.vulnerabilitiesList = []
                for (const value of res.data.results) {
                   this.vulnerabilitiesList.push({
                      name: { vul_name: value.name },
                      sev: value.stats.severity_count,
                      id: value.id,
                      url: '/projects/individual_application/' + value.id + '/'
                    })
                }
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
            this.fetchData()
          }
        } 
      },
      createApplication() {
        if (this.param && this.org && this.token) {
          this.appName  = ''
          this.appLogo = ''
          this.appHostType = null
          this.appUrl = ''
          this.appPlatformTags = null
          this.appIpv4 = ''
          this.appOsInfo =''
          this.$refs.fileinput.reset();
          axios.get('/hosttypes/')
            .then(res => {
              this.appTargetOption = res.data
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
          axios.get('/platforms/')
            .then(res => {
              this.appPlatformOption = res.data
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
          this.$refs.createApplicationModal.show()
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
      closeCreateApplication() {
        this.$refs.createApplicationModal.hide()
      },
      submitCreateApplication() {
        if (this.param && this.org && this.token) {
          this.isClicked = true
          const form_data = new FormData()
          form_data.append('name', this.appName)
          form_data.append('logo', this.appLogo)
          form_data.append('host_type', this.appHostType)
          form_data.append('url', this.appUrl)
          form_data.append('platform_tags', this.appPlatformTags)
          form_data.append('ipv4', this.appIpv4)
          form_data.append('os_info', this.appOsInfo)
          form_data.append('project', this.projectId)
          form_data.append('org', this.org)
          axios.put('/applications/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.reloadPage = true
              this.$refs.createApplicationModal.hide()
              this.isLoading = true
              // this.$router.go()
              // this.$router.push('/projects/individual_project/' + this.projectId + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The application has been created successfully!',
                position: 'top right'
              })
              this.isClicked = false
              this.reloadPage = false
              this.fetchData()

            }).catch(error => {
              this.isClicked = false
              var status_info = error.response.status
              if(status_info === 400){
                  this.$notify({
                    group: 'foo',
                    type: 'error',
                    title: 'error',
                    text: 'Error in creation of application',
                    position: 'top right'
                })
              }
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
     async updateApplication(event) {
        if (event.show && event.id && this.param && this.org && this.token) {
          this.$refs.updateApplicationModal.show()
         await axios.get('/applications/' + event.id + '/')
            .then(res => {
                this.appUpdateName = res.data.name
                this.updateApplicationId = event.id
                this.appUpdateHostType = res.data.host_type
                this.appUpdateUrl = res.data.url
                this.appUpdatePlatformTags = res.data.platform_tags
                this.appUpdateIpv4 = res.data.ipv4
                this.appUpdateOsInfo = res.data.os_info
                const updatelogoSplit = res.data.logo.split('/')
                const logoSplit = updatelogoSplit.pop()
                this.appUpdateOldLogoName = logoSplit
                // this.updateTags = []
                // for (const lan of lang){
                //   this.updateTags.push({text : lan})
                // }
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
          await axios.get('/platforms/')
            .then(res => {
              this.appPlatformOption = res.data
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
          // await axios.get('/applications/' + event.id + '/')
          //   .then(res => {
          //     this.appUpdateName = res.data.name
          //     this.updateApplicationId = event.id
          //     this.appUpdateHostType = res.data.host_type
          //     this.appUpdateUrl = res.data.url
          //     const lang =  res.data.languages.split(",")
          //     this.updateTags = []
          //     for (const lan of lang){
          //       this.updateTags.push({text : lan})
          //     }
          //     this.appUpdateIpv4 = res.data.ipv4
          //     this.appUpdateOsInfo = res.data.os_info
          //     for (const value of this.appGroupsOption) {
          //       if (value.value === res.data.group[0]) {
          //         this.appUpdateGroup = { 'value': res.data.group[0], 'label': value.label }
          //       }
          //     }
          //     const updatelogoSplit = res.data.logo.split('/')
          //     const logoSplit = updatelogoSplit.pop()
          //     this.appUpdateOldLogoName = logoSplit
          //   }).catch(error => {
          //     // if (error.response.status === 404) {
          //     //   this.$router.push('/not_found')
          //     // } else if (error.response.status === 403) {
          //     //   this.$router.push('/forbidden')
          //     // } else {
          //     //   this.$router.push('/error')
          //     // }
          //   })
          this.appTargetOption = []
          axios.get('/hosttypes/')
            .then(res => {
              this.appTargetOption = res.data
            }).catch(error => {
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
      closeUpdateApplication() {
        this.$refs.updateApplicationModal.hide()
      },
      submitUpdateApplication() {
        if (this.param && this.org && this.token) {
          const form_data = new FormData()
          if (this.appUpdateLogo) {
            form_data.append('logo', this.appUpdateLogo)
          }
          form_data.append('name', this.appUpdateName)
          form_data.append('host_type', this.appUpdateHostType)
          form_data.append('url', this.appUpdateUrl)
          form_data.append('platform_tags', this.appUpdatePlatformTags)
          form_data.append('ipv4', this.appUpdateIpv4)
          form_data.append('os_info', this.appUpdateOsInfo)
          form_data.append('project', this.projectId)
          form_data.append('org', this.org)
          axios.post('/applications/' + this.updateApplicationId + '/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.reloadPage = true
              this.isLoading = true
              this.$refs.updateApplicationModal.hide()
              // this.$router.go()
              // this.$router.push('/projects/individual_project/' + this.projectId + '/')
              this.isLoading = true
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'success',
                text: 'The application has been updated Successfully!',
                position: 'top right'
              })
              this.reloadPage = false
              this.fetchData()

            }).catch(error => {
               var status_info = error.response.status
              if(status_info === 400){
                  this.$notify({
                    group: 'foo',
                    type: 'error',
                    title: 'error',
                    text: 'Error in updation of application',
                    position: 'top right'
                })
              }
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
      beforeDeleteModal(event) {
        this.$refs.beforedeleteApplicationModal.show()
        this.deleteApplicationId = event.id
      },
      beforeCloseDeleteApplication() {
        this.$refs.beforedeleteApplicationModal.hide()
      },
      closeDeleteApplication() {
        this.$refs.beforedeleteApplicationModal.hide()
      },
      BeforeSubmitDeleteApplication() {
        this.$refs.deleteApplicationModal.show()
      },
      submitDeleteApplication() {
        if (this.param && this.org && this.token && this.deleteApplicationId) {
          axios.delete('/applications/' + this.deleteApplicationId + '/')
            .then(res => {
              this.$refs.deleteApplicationModal.hide()
              this.reloadPage = true
              this.isLoading = true
              this.$router.push('/projects/individual_project/' + this.projectId)
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'success',
                text: 'The aplication has been deleted successfully!',
                position: 'top right'
              })
              this.reloadPage = false
              this.fetchData()
            }).catch(error => {
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

  .label {
    font-family: 'Avenir';
    font-size: 16px;
    line-height: 1.33;
    color: #000000;
  }

  .inline-form-control {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #ddd;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
  }

  .delete-header {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 500;
    line-height: 0.99;
    text-align: center;
    color: #232325;
  }

  .delete-sub {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 400;
    line-height: 0.99;
    text-align: center;
    color: #232325;
  }
</style>

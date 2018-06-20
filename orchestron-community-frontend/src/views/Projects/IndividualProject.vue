<template>
    <div>
        <b-container fluid>
            <loading :active.sync="isLoading" :can-cancel="true"></loading>
            <headers :name="projectName" :createdOn="projectCreatedOn" :logo="projectLogo"></headers>
            <br>
            <common-table
              :pageCount="applicationCount"
              :dataItems="vulnerabilitiesList"
              :headerTitle="headerTitles"
              @createModal="createApplication"
              @updateModal="updateApplication($event)"
              @deleteModal="beforeDeleteModal($event)"></common-table>
            <b-modal ref="createApplicationModal" title="Create Application" centered size="lg">
                <div>
                    <form @submit.prevent="submitCreateApplication">
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Name:</label>
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
                                <label class="label">Target Type:</label>
                                <b-col sm="12">
                                  <v-select
                                    :options="appTargetOption"
                                    v-model="appHostType"
                                    placeholder="Select Target Type"
                                    :state="!$v.appHostType.$invalid"></v-select>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">Platform Type:</label>
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
                                <label class="label">URL:</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appUrl"
                                      type="text"
                                      class="inline-form-control"
                                      :state="!$v.appUrl.$invalid"
                                      placeholder="http://example.com">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">IPv4:</label>
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
                              <label class="label">OS Info:</label>
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
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeCreateApplication() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitCreateApplication() "
                                v-if="!$v.appName.$invalid && !$v.appLogo.$invalid && !$v.appHostType.$invalid
                            && !$v.appPlatformTags.$invalid && !$v.appUrl.$invalid && !$v.appIpv4.$invalid && !$v.appOsInfo.$invalid">
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
                                <label class="label">Name:</label>
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
                                <label class="label">Target Type:</label>
                                <b-col sm="12">
                                  <v-select
                                    :options="appTargetOption"
                                    v-model="appUpdateHostType"
                                    :state="!$v.appUpdateHostType.$invalid"></v-select>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">Platform Type:</label>
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
                                <label class="label">URL:</label>
                                <b-col sm="12">
                                    <b-form-input
                                      v-model="appUpdateUrl"
                                      type="text"
                                      class="inline-form-control"
                                      :state="!$v.appUpdateUrl.$invalid"
                                      placeholder="http://example.com">
                                    </b-form-input>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">IPv4:</label>
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
                              <label class="label">OS Info:</label>
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
              <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeUpdateApplication() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitUpdateApplication() "
                                v-if="!$v.appUpdateName.$invalid && !$v.appUpdateHostType.$invalid
                            && !$v.appUpdatePlatformTags.$invalid && !$v.appUpdateUrl.$invalid && !$v.appUpdateIpv4.$invalid
                            && !$v.appUpdateOsInfo.$invalid">
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
                <b-col col="12" slot="modal-footer">
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
                <b-col col="12" slot="modal-footer">
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
        applicationCount: 0
      }
    },
    validations: {
      appName: {
        required,
        minLength: minLength(1)
      },
      appLogo: {
        required
      },
      appHostType: {
        required
      },
      appPlatformTags: {
        required
      },
      appUrl: {
        required,
        url
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
      appUpdateUrl: {
        required,
        url
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
      this.fetchData()
    },
    updated() {
      this.$nextTick(function() {
        if (this.isLoading) {
          this.vulnerabilitiesList = []
          this.fetchData()
          this.isLoading = false
        }
      })
    },
    methods: {
      fetchData() {
        if (this.param && this.org && this.token) {
          axios.get('/projects/' + this.param + '/?&severity=1&applications=1')
            .then(res => {
              this.applicationCount = res.data.applications_count
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
              for (const value of res.data.applications) {
                this.vulnerabilitiesList.push({
                  name: { vul_name: value.fields.name },
                  sev: value.stats.severity_count.severity,
                  id: value.fields.id,
                  url: '/projects/individual_application/' + value.fields.id + '/'
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
      createApplication() {
        if (this.param && this.org && this.token) {
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
              this.$refs.createApplicationModal.hide()
              this.isLoading = true
              this.$router.push('/projects/individual_project/' + this.projectId + '/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Application',
                text: 'The Application has been created Successfully!',
                position: 'top right'
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
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
      updateApplication(event) {
        if (event.show && event.id && this.param && this.org && this.token) {
          this.$refs.updateApplicationModal.show()
          axios.get('/applications/' + event.id + '/')
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
              this.$refs.updateApplicationModal.hide()
              this.isLoading = true
              this.$router.push('/projects/individual_project/' + this.projectId + '/')
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'Application',
                text: 'The application has been updated Successfully!',
                position: 'top right'
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
              this.isLoading = true
              this.$router.push('/projects/individual_project/' + this.projectId)
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'Application',
                text: 'The aplication has been deleted Successfully!',
                position: 'top right'
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

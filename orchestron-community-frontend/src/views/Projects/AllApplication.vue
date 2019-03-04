<template>
    <div>
        <b-container fluid>
          <loading :active.sync="isLoading" :can-cancel="true"></loading>
          <loading :active.sync="isDataLoading" :can-cancel="true"></loading>
          <common-table 
         :pageCount="applicationCount"
          :dataItems="data_showing"
          :headerTitle="headerTitles"
          @clickPagination="clickPaginations($event)"
          @updateModal="updateApplication($event)"
          @deleteModal="beforeDeleteModal($event)"
          :create="false"
           ></common-table>
        </b-container>
          <!-- create an application -->
      

            <!--Update Modal-->
            <b-modal ref="updateApplicationModal" title="Update Application" centered size="lg">
                <div>
                    <form @submit.prevent="submitUpdateApplication">
                        <b-row class="my-1">
                            <b-col cols="6">
                                <label class="label">Name: *</label>
                                <p v-if="appUpdateNameError" class="error"> * {{ appUpdateNameError }}</p>
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
                                <p v-if="appUpdateLogoError" class="error"> * {{ appUpdateLogoError }}</p>
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
                                <p v-if="appUpdateHostTypeError" class="error"> * {{ appUpdateHostTypeError }}</p>
                                <b-col sm="12">
                                  <v-select
                                    :options="appTargetOption"
                                    v-model="appUpdateHostType"
                                    :state="!$v.appUpdateHostType.$invalid"></v-select>
                                </b-col>
                            </b-col>
                          <b-col cols="6">
                              <label class="label">Platform Type: *</label>
                              <p v-if="appUpdatePlatformTagsError" class="error"> * {{ appUpdatePlatformTagsError }}</p>
                              <b-col sm="12">
                                <v-select
                                  :options="appPlatformOption"
                                  v-model="appUpdatePlatformTags"
                                  :state="!$v.appUpdatePlatformTags.$invalid"></v-select>
                                <!-- <vue-tags-input
                                  v-model="updateTag"
                                  :tags="updateTags"
                                  :autocomplete-items="autocompleteItems"
                                  @tags-changed="newTags => updateTags = newTags">
                                </vue-tags-input> -->
                              </b-col>
                          </b-col>

                        </b-row>
                        <br>
                      <b-row class="my-1">
                          <b-col cols="6">
                                <label class="label">URL: *</label>
                                <p v-if="appUpdateUrlError" class="error"> * {{ appUpdateUrlError }}</p>
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
                              <label class="label">IPv4: *</label>
                              <p v-if="appUpdateIpv4Error" class="error"> * {{ appUpdateIpv4Error }}</p>
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
                              <p v-if="appUpdateOsInfoError" class="error"> * {{ appUpdateOsInfoError }}</p>
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
                        <button type="button"
                                class="btn btn-orange-submit"
                                data-dismiss="modal" @click=" submitUpdateApplication() "
                                v-if="!$v.appUpdateName.$invalid && !$v.appUpdateHostType.$invalid && !$v.appUpdateUrl.$invalid && !$v.appUpdateIpv4.$invalid && !$v.appUpdateOsInfo.$invalid"
                                >
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

        <!-- <v-tour name="orchyTour" :steps="steps"></v-tour> -->
    </div>
</template>

<script>
  import CommonTable from '@/components/Projects/CommonTable'
  import axios from '@/utils/auth'
  import { required, minLength, url, ipAddress  } from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import { notValidUser } from '@/utils/checkAuthUser'

export default {
    name: 'AllApplication',
    components: {
      CommonTable,
      Loading
    },
    data() {
      return {
        applicationCount: 0,
        applicationList: [],
        headerTitles: 'All Application List',
        isLoading: false,
        timeout: 1000,
        org:1,
        token: '',
        isDataLoading: false,
        isLoading: false,
        appname: '',
        appId: '',
        paginatedapplicationsList: [],
        applicationsList: [],
        appLogoError: '',
        appHostTypeError: '',
        appLogo: '',
        appHostType: '',
        appPlatformTagsError: '',
        tag:'',
        tags:[],
        appUrlError:'',
        appUrl: '',
        appIpv4Error: '',
        appIpv4: '',
        appOsInfoError: '',
        appOsInfo: '',
        appGroup: [],
        appGroupsOption: [],
        appUpdateGroup: [],
        appUpdateOsInfo: '',
        appUpdateIpv4: '',
        appUpdateUrl: '',
        appUpdatePlatformTags: [],
        appUpdateHostType: '',
        appUpdateName : '',
        appNameError: '',
        appTargetOption: [],
        autocompleteItems: [],
        appGroupError : '',
        appUpdateGroupError: '',
        appUpdateOsInfoError: '',
        appUpdateUrlError : '',
        appUpdateIpv4Error : '',
        updateTag: '',
        updateTags: [],
        appUpdatePlatformTagsError: '',
        appUpdateHostTypeError : '',
        appUpdateOldLogoName : '',
        appUpdateLogo : '',
        appUpdateLogoError : '',
        appUpdateNameError : '',
        projectId : '',
        typeDelete : '',
        deleteApplicationId : '',
        data_showing: [],
        is_updated: false,
        isPageLoading: false,
      }
    },
     validations: {
      appName: {
        required,
        minLength: minLength(1)
      },
      appLogo: {

      },
      appHostType: {
        required
      },
      tag: {
        required
      },
      appUrl: {
        required
        // url
      },
      appIpv4: {
        required,
        ipAddress
      },
      appOsInfo: {
        required
      },
      appGroup: {
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
      },
      appUpdateGroup: {
        required
      }
    },
    created() {
     
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      // this.param = this.$route.params.projectId  
      this.fetchData()
    },
    updated() {
      if (this.isLoading) {
        this.$nextTick(function() {
            this.isLoading = false
        })
      }
      if(this.is_updated){
        this.$nextTick(function() {
            this.fetchData()
            this.is_updated = false
        })
      }
       if (this.isPageLoading) {
        this.$nextTick(() => {
          this.data_showing = this.paginatedapplicationsList
        })
        this.isPageLoading = false
      }
    },
    methods: {
      fetchData() {
        if (this.org && this.token) {
          this.isDataLoading = true
          setTimeout(() => {
          axios.get('/applications/list/')
            .then(res => {
              this.isDataLoading = true
               this.applicationsList = []
               this.paginatedapplicationsList = []
               this.data_showing = []
                this.applicationCount = res.data.length
                  for (const value of res.data) {
                    this.applicationsList.push({
                      name: { vul_name: value.name },
                      sev: value.stats.severity_count,
                      id: value.id,
                      url: '/projects/individual_application/' + value.id + '/',
                      sevUrl: '/projects/individual_application/' + value.id + '/severity_wise/'
                    })
                  }
                  this.data_showing = this.applicationsList.slice(0, 5)
                  this.isDataLoading = false
            }).catch(error => {
              if (error.response.status === 404) {
                this.$router.push('/not_found')
              } else if (error.response.status === 403) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
            this.isDataLoading = false
        }, this.timeout);

         this.appPlatformOption = []
          axios.get('/platforms/')
            .then(res => {
              this.appPlatformOption = res.data
            }).catch(error => {
              if (error.response.status === 404) {
                this.$router.push('/not_found')
              } else if (error.response.status === 403) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        }
        else {
          notValidUser()
          this.$router.push('/')
        }
      },
     clickPaginations(event) {
          console.log("event fired")
          if (event.page) {
            if (event.page > 1) {
               this.applicationCount = this.applicationsList.length
                var page_no = event.page
                this.paginatedapplicationsList = this.applicationsList.slice(5*(page_no-1), 5*(page_no))
                this.data_showing =  this.paginatedapplicationsList
                this.isPageLoading = true
                this.isLoading = false
                // this.isDataLoading = false
              // this.isDataLoading = true
              //   var page_no = event.page
              //   console.log("33333", event.page)
              //   this.paginatedapplicationsList = this.applicationsList.slice(5*(page_no-1), 5*(page_no))
              //   console.log("paginatedapplicationsList", this.paginatedapplicationsList)
              //   this.data_showing =  this.paginatedapplicationsList
              //   this.isLoading = true
              //   this.isDataLoading = true

            } else {
              this.fetchData()
            }
          }
          else {
            // notValidUser()
            // this.$router.push('/')
          }
        },

       async  updateApplication(event) {
        if (event.show && event.id  && this.org && this.token) {
          this.$refs.updateApplicationModal.show()
          // this.appGroupsOption = []
          // this.appUpdateGroup = false
          // await axios.get('/groups/list/')
          //   .then(res => {
          //     for (const value of res.data) {
          //       this.appGroupsOption.push({ value: value.id, label: value.name })
          //     }
          //   }).catch(error => {
          //     if (error.response.status === 403) {
          //       this.$router.push('/not_found')
          //     } else if (error.response.status === 404) {
          //       this.$router.push('/forbidden')
          //     } else {
          //       this.$router.push('/error')
          //     }
          //   })
          await axios.get('/applications/' + event.id + '/')
            .then(res => {
              console.log("update app", res.data)
              this.appUpdateIpv4 = res.data.ipv4
              this.appUpdatePlatformTags = res.data.platform_tags
              this.projectId = res.data.project
              this.appUpdateName = res.data.name
              this.updateApplicationId = event.id
              this.appUpdateHostType = res.data.host_type
              this.appUpdateUrl = res.data.url
              this.appUpdateOsInfo = res.data.os_info
              // const lang =  res.data.languages.split(",")
              // this.updateTags = []
              // for (const lan of lang){
              //   this.updateTags.push({text : lan})
              // }
              
              
              // for (const value of this.appGroupsOption) {
              //   if (value.value === res.data.group[0]) {
              //     this.appUpdateGroup = { 'value': res.data.group[0], 'label': value.label }
              //   }
              // }
              const updatelogoSplit = res.data.logo.split('/')
              const logoSplit = updatelogoSplit.pop()
              this.appUpdateOldLogoName = logoSplit
            }).catch(error => {
              // if (error.response.status === 404) {
              //   this.$router.push('/not_found')
              // } else if (error.response.status === 403) {
              //   this.$router.push('/forbidden')
              // } else {
              //   this.$router.push('/error')
              // }
            })
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
          // this.appPlatformOption = []
          // axios.get('/platforms/')
          //   .then(res => {
          //     this.appPlatformOption = res.data
          //   }).catch(error => {
          //     if (error.response.status === 404) {
          //       this.$router.push('/not_found')
          //     } else if (error.response.status === 403) {
          //       this.$router.push('/forbidden')
          //     } else {
          //       this.$router.push('/error')
          //     }
          //   })
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
       submitUpdateApplication() {
        if (this.org && this.token) {
          const form_data = new FormData()
          if (this.appUpdateLogo) {
            form_data.append('logo', this.appUpdateLogo)
          }
        const platforms = []
          for(const plat of this.updateTags){
            platforms.push(plat.text)
          }
          form_data.append('name', this.appUpdateName)
          form_data.append('host_type', this.appUpdateHostType)
          form_data.append('url', this.appUpdateUrl)
          form_data.append('languages', platforms.toString())
          form_data.append('ipv4', this.appUpdateIpv4)
          form_data.append('os_info', this.appUpdateOsInfo)
          if(this.appUpdateGroup.value){
            form_data.append('group', this.appUpdateGroup.value)
          }
          form_data.append('project', this.projectId)
          form_data.append('org', this.org)
          axios.post('/applications/' + this.updateApplicationId + '/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.$refs.updateApplicationModal.hide()

              // this.is_updated = true
              this.$router.push('/projects/individual_project/' + this.projectId + '/')
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'Application',
                text: 'The application has been updated Successfully!',
                position: 'top right'
              })
            }).catch(error => {
              if (error.response.status === 400) {
                if (error.response.data.name !== undefined && error.response.data.name.length > 0) {
                  if (error.response.data.name[0] === 'application with this name already exists.') { this.appUpdateNameError = 'application with this name already exists.' }
                } else {
                  this.appUpdateNameError = 'Please enter a valid name'
                }
                if (error.response.data.group !== undefined && error.response.data.group.length > 0) {
                  this.appUpdateGroupError = 'Please select a valid group'
                }
                if (error.response.data.logo !== undefined && error.response.data.logo.length > 0) {
                  this.appUpdateLogoError = 'Please enter a valid logo'
                }
                if (error.response.data.host_type !== undefined && error.response.data.host_type.length > 0) {
                  this.appUpdateHostTypeError = 'Please select a valid Target Type'
                }
                if (error.response.data.url !== undefined && error.response.data.url.length > 0) {
                  this.appUpdateUrlError = 'Please enter a valid URL'
                }
                if (error.response.data.languages !== undefined && error.response.data.languages.length > 0) {
                  this.appUpdatePlatformTagsError = 'Please select a valid Platform'
                }
                if (error.response.data.ipv4 !== undefined && error.response.data.ipv4.length > 0) {
                  this.appUpdateIpv4Error = 'Please enter a valid IpV4'
                }
                if (error.response.data.os_info !== undefined && error.response.data.os_info.length > 0) {
                  this.appUpdateOsInfoError = 'Please enter a valid OS Info'
                }
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
      beforeDeleteModal(event) {
        this.typeDelete = ''
        this.$refs.beforedeleteApplicationModal.show()
        this.deleteApplicationId = event.id
      },
      beforeCloseDeleteApplication() {
        this.typeDelete = ''
        this.$refs.beforedeleteApplicationModal.hide()
      },
      closeDeleteApplication() {
        this.typeDelete = ''
        this.$refs.beforedeleteApplicationModal.hide()
      },
      BeforeSubmitDeleteApplication() {
        this.$refs.deleteApplicationModal.show()
      },
      submitDeleteApplication() {
        if (this.typeDelete === 'DELETE') {
          if (this.org && this.token && this.deleteApplicationId) {
            axios.delete('/applications/' + this.deleteApplicationId + '/')
              .then(res => {
                this.$refs.deleteApplicationModal.hide()
                this.isLoading = true
                this.$router.go('/all_applications/')
                this.$notify({
                  group: 'foo',
                  type: 'error',
                  title: 'Application',
                  text: 'The aplication has been deleted Successfully!',
                  position: 'top right'
                })
              }).catch(error => {
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

<template>
    <div>
        <b-container fluid>
          <loading :active.sync="isLoading" :can-cancel="true"></loading>
            <web-hook-common-table
            :headerTitle=" 'List of Webhooks' "
            @clickPagination="clickPagination($event)" 
            :dataItems="webhookData"
            @createModal="createWebhook"
            @updateModal="updateWebhook($event)"
            @copyModal="copyWebhook($event)"
            @deleteModal="deleteWebhook($event)" :pageCount="webhookCount"></web-hook-common-table>
            <!-- {{webhookPaginatedData}} -->
            <!--Create-->
            <b-modal
                ref="createWebhookModal"
                title="Create Webhook"
                size="lg"
                centered>
                <div>
                    <form @submit.prevent="submitCreateWebhook">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="webhookName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Webhook Name" :state="!$v.webhookName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Application:</label></b-col>
                            <b-col sm="10">
                                <v-select
                                  :options="applicationOption"
                                  label="label"
                                  placeholder="Select Application"
                                  v-model="application"
                                  :state="!$v.application.$invalid"></v-select>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Tool:</label></b-col>
                            <b-col sm="10">
                                <v-select
                                  :options="toolOption"
                                  placeholder="Select Tool"
                                  v-model="tool"
                                  :state="!$v.tool.$invalid"></v-select>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeCreateWebhook() "> Close</button>
                        <button type="button"
                                class="btn btn-orange-submit pull-right"
                                data-dismiss="modal" @click=" submitCreateWebhook()" v-if="!$v.webhookName.$invalid && !$v.application.$invalid && !$v.tool.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Update-->
            <b-modal
                ref="updateWebhookModal"
                title="Update Webhook"
                size="lg"
                centered>
                <div>
                    <form @submit.prevent="submitUpdateWebhook">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="updateWebhookName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Webhook Name" :state="!$v.updateWebhookName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Application:</label></b-col>
                            <b-col sm="10">
                                <v-select
                                  :options="applicationOption"
                                  v-model="updateApplication"
                                  :state="!$v.updateApplication.$invalid"></v-select>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Tool:</label></b-col>
                            <b-col sm="10">
                                <v-select
                                  :options="toolOption"
                                  v-model="updateTool"
                                  :state="!$v.updateTool.$invalid"></v-select>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeUpdateWebhook() "> Close</button>
                        <button type="button"
                                class="btn btn-orange-submit pull-right"
                                data-dismiss="modal" @click=" submitUpdateWebhook()" v-if="!$v.updateWebhookName.$invalid && !$v.updateApplication.$invalid && !$v.updateTool.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Delete-->
            <b-modal ref="deleteWebhookModal" title="Delete Webhook" centered size="lg">
                <div>
                    <form @submit.prevent="submitDeleteWebhook">
                        <input type="hidden" v-model="webhookId">
                        <p class="delete-header">Are you sure want to delete this webhook ?</p>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeDeleteWebhook() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitDeleteWebhook() ">
                        Delete
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Copy-->
            <b-modal ref="copyWebhookModal" title="Copy Webhook" centered size="lg">
                <b-row>
                  <b-col cols="12">
                <div style="background-color:#2b2b2b; border-radius: 5px; height:50px;width: 100%;">
                  <p style="text-align:left;vertical-align: middle;padding-top: 2%;" class="word-wrap">
                    <pre> <span class="webhook-label">Webhook Id : </span>  <span class='webhook'>{{ webhookId }}</span></pre>
                  </p>
                  <br>
                </div>
              <br>
                  </b-col>
                  <b-col cols="12">
              <div style="background-color: #2b2b2b; border-radius: 5px; height:50px;display: table;width: 100%;">
                  <p style="vertical-align: middle;width: 100%;padding-top: 2%;" class="word-wrap">
                    <span class="webhook-label" style="padding:7px;">User Token : </span>
                   <span class='webhook'><label style="word-break: break-all;padding:7px;">{{ userToken }}</label></span>
                  </p>
                  <br>
                </div>
              <br>
                    </b-col>
                </b-row>
              <div style="background-color: #2b2b2b; border-radius: 5px; height:100px;width: 100%;">
                  <p style="text-align:left;vertical-align: middle; padding-top: 2%;">
                    <span class="webhook-label" style="padding:7px;">Curl Command (File Processing) : </span>
                    <span class='webhook'>
                       {{curlCmd}}<label>{{ webhookId }}</label>
                    </span>
                  </p>
                  <br>
                </div>
              <br>
              <div style="background-color: #2b2b2b; border-radius: 5px; height:100px;display: table;width: 100%;">
                  <p style="text-align:left;vertical-align: middle;padding-top: 2%;">
                   <span class="webhook-label" style="padding:7px;"> Curl Command (JSON Processing) : </span>
                    <span class='webhook'>
                      {{jsonCmd}}<label>{{ webhookId }}</label>
                    </span>
                  </p>
                  <br>
                </div>
                <b-col col="12" slot="modal-footer">
                    <p class="importent-text">* (Optional) To fetch engagement id go to Engagements</p>
                </b-col>
            </b-modal>
        </b-container>
    </div>
</template>

<script>
  import WebHookCommonTable from '@/components/webhooks/CommonTable'
  import axios from '@/utils/auth'
  import { required, minLength } from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import { notValidUser } from '@/utils/checkAuthUser'

  export default {
    name: 'WebHook',
    components: {
      WebHookCommonTable,
      Loading
    },
    data() {
      return {
        isLoading: false,
        isPaginated: false,
        webhookCount: 0,
        webhookData: [],
        applicationOption: [],
        webhookPaginatedData: [],
        toolOption: [],
        webhookName: '',
        application: '',
        tool: '',
        webhookId: '',
        updateWebhookName: '',
        updateApplication: '',
        updateApplicationId: '',
        updateTool: '',
        userToken: '',
        curlCmd: 'curl -H "Authorization: Token " -H "X-Engagement-ID: <engagement_id>" -H "Scan-Name: <scan_name>"-v -F file=@<file_path> http://127.0.0.1/api/webhook/post/',
        jsonCmd: 'curl -H "Authorization: Token " -H "X-Engagement-ID: <engagement_id>" -H "Scan-Name: <scan_name>" -d \'{"vuls":<json_dictionary>}\' http://127.0.0.1/api/webhook/post/'
      }
    },
    validations: {
      webhookName: {
        required,
        minLength: minLength(1)
      },
      application: {
        required
      },
      tool: {
        required
      },
      updateWebhookName: {
        required,
        minLength: minLength(1)
      },
      updateApplication: {
        required
      },
      updateTool: {
        required
      }
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.fetchData()
    },
    updated() {
      if (this.isLoading) {
        this.$nextTick(() => {
          this.webhookData = []
          this.fetchData()
        })
        this.isLoading = false
      }
    if (this.isPaginated) {
        this.$nextTick(() => {
          this.webhookData = []
          this.webhookData = this.webhookPaginatedData
        })
        this.isPaginated = false
      }

    },
    methods: {
      fetchData() {
        if (this.org && this.token) {
          axios.get('/applications/list/')
            .then(res => {
              this.applicationOption = []
              // this.webhookCount = 0
              // this.webhookCount = res.data.count
              for (const value of res.data) {
                this.applicationOption.push({ value: value.id, label: value.name })
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
          axios.get('/webhooks/')
            .then(res => {
              this.webhookData = []
               this.webhookCount = res.data.count
              for (const value of res.data.results) {
                let appName = ''
                for (const app of this.applicationOption) {
                  if (value.application === app.value) {
                    appName = app.label
                  }
                }
                this.webhookData.push({ 'name': value.name, 'app': appName, 'tool': value.tool, 'id': value.hook_id })
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
     clickPagination(event) {
      if (event.page) {
        if (event.page > 1) {
          // axios.get('/applications/')
          //   .then(res => {
          //     this.applicationOption = []
          //     for (const value of res.data) {
          //       this.applicationOption.push({ value: value.id, label: value.name })
          //     }
          //   }).catch(error => {
          //     if (error.response.status === 404) {
          //       this.$router.push('/not_found')
          //     } else if (error.response.status === 403) {
          //       this.$router.push('/forbidden')
          //     } else {
          //       this.$router.push('/error')
          //     }
          //   })
          axios.get('/webhooks/?page='+ event.page)
            .then(res => {
              this.webhookPaginatedData = []
              for (const value of res.data.results) {
                let appName = ''
                for (const app of this.applicationOption) {
                  if (value.application === app.value) {
                    appName = app.label
                  }
                }
                
                this.webhookPaginatedData.push({ 'name': value.name, 'app': appName, 'tool': value.tool, 'id': value.hook_id })
                this.webhookData = this.webhookPaginatedData
                this.isPaginated = true
              }
            }).catch(error => {
              if (error.response.status === 404) {
                this.$router.push('/not_found')
              } else if (error.response.status === 403) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
          //  this.isPaginated = true
        } else {
          this.fetchData()
        }
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
      createWebhook() {
        if (this.org && this.token) {
          this.$refs.createWebhookModal.show()
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
      closeCreateWebhook() {
        this.$refs.createWebhookModal.hide()
      },
      submitCreateWebhook() {
        if (this.org && this.token) {
          const form_data = new FormData()
          form_data.append('name', this.webhookName)
          form_data.append('application', this.application.value)
          form_data.append('tool', this.tool)
          axios.put('/webhooks/', form_data)
            .then(res => {
              this.$refs.createWebhookModal.hide()
              this.isLoading = true
              this.$router.push('/webhooks/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Webhook',
                text: 'The Webhook has been created Successfully!',
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
      updateWebhook(event) {
        this.webhookId = event.id
        if (this.org && this.token && event.id) {
          this.$refs.updateWebhookModal.show()
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
          axios.get('/webhooks/' + this.webhookId + '/')
            .then(res => {
              this.updateWebhookName = res.data.name
              this.updateTool = res.data.tool
              if (res.data.application) {
                axios.get('/applications/')
                  .then(resp => {
                    for (const app of resp.data.results) {
                      if (res.data.application === app.id) {
                        this.updateApplication = app.name
                        this.updateApplicationId = app.id
                      }
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
      closeUpdateWebhook() {
        this.$refs.updateWebhookModal.hide()
      },
      submitUpdateWebhook() {
        if (this.org && this.token && this.webhookId) {
          let updateAppId = ''
          if (this.updateApplication.value) {
            updateAppId = this.updateApplication.value
          } else {
            updateAppId = this.updateApplicationId
          }
          const form_data = new FormData()
          form_data.append('name', this.updateWebhookName)
          form_data.append('application', updateAppId)
          form_data.append('tool', this.updateTool)
          axios.post('/webhooks/' + this.webhookId + '/', form_data)
            .then(res => {
              this.$refs.updateWebhookModal.hide()
              this.isLoading = true
              this.$router.push('/webhooks/')
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'Webhook',
                text: 'The Webhook has been updated Successfully!',
                position: 'top right'
              })
              this.webhookId = ''
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
      deleteWebhook(event) {
        this.$refs.deleteWebhookModal.show()
        this.webhookId = event.id
      },
      closeDeleteWebhook() {
        this.$refs.deleteWebhookModal.hide()
      },
      submitDeleteWebhook() {
        if (this.org && this.token && this.webhookId) {
          axios.delete('/webhooks/' + this.webhookId + '/')
            .then(res => {
              this.$refs.deleteWebhookModal.hide()
              this.isLoading = true
              this.$router.push('/webhooks/')
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'Webhook',
                text: 'The webhook has been deleted Successfully!',
                position: 'top right'
              })
              this.webhookId = ''
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
      copyWebhook(event) {
        this.webhookId = event.id
        this.$refs.copyWebhookModal.show()
        this.userToken = localStorage.getItem('token')
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
    /*height: 40px;*/

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

  .label{
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
  .webhook{
    color: #ffb648;
    word-wrap:break-word;
    font-family: 'Avenir';
    font-size: 14px;
    white-space: pre-wrap;
   white-space: -moz-pre-wrap;
   white-space: -pre-wrap;
   white-space: -o-pre-wrap;
   word-wrap: break-word;
  }
  .webhook-label{
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 500;
    line-height: 0.99;
    text-align: left;
    color: #ffb648;

  }
  .word-wrap {
   white-space: pre-wrap;
   white-space: -moz-pre-wrap;
   white-space: -pre-wrap;
   white-space: -o-pre-wrap;
   word-wrap: break-word;
}
  .importent-text{
    color: #ff542c;
    text-align: center;
  }
</style>

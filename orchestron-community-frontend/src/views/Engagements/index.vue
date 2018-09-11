<template>
    <div>
      <b-container fluid>
        <loading :active.sync="isLoading" :can-cancel="true"></loading>
        <common-table :pageCount="engagementsCount" :dataItems="engagementList" :headerTitle="headerTitles"
            @createModal="createEngagement"
            @updateModal="updateEngagement($event)"
            @deleteModal="deleteEngagement($event)"
            @clickPagination="clickPagination($event)"
            ></common-table>

        <!--create-->
        <b-modal
                ref="createEngagementModal"
                title="Create Engagement"
                size="lg"
                centered>
                <div>
                    <form @submit.prevent="submitCreateEngagement">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="engagementName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Engagement Name" :state="!$v.engagementName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Description:</label></b-col>
                            <b-col sm="10">
                                <b-form-textarea
                                   v-model="engagementDesc"
                                   placeholder="Enter Description"
                                   :rows="3"
                                   :max-rows="6" :state="!$v.engagementDesc.$invalid">
                                </b-form-textarea>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Application:</label></b-col>
                            <b-col sm="10">
                                <v-select
                                  :options="applicationOption"
                                  placeholder="Select Application"
                                  v-model="application"
                                  :state="!$v.application.$invalid"></v-select>
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Start Date:</label></b-col>
                            <b-col sm="10">
                                <date-picker
                                  v-model="engagementDateRange"
                                  range :shortcuts="shortcuts"
                                  format="yyyy-MM-dd"
                                  lang="en" width="100%"
                                  :not-before="today" :state="!$v.engagementDateRange.$invalid"></date-picker>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeCreateEngagement() "> Close</button>
                        <button type="button"
                                class="btn btn-orange-submit pull-right"
                                data-dismiss="modal"
                                @click=" submitCreateEngagement() "
                                v-if="!$v.engagementName.$invalid && !$v.engagementDesc.$invalid && !$v.application.$invalid && !$v.engagementDateRange.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>

        <!--update-->
        <b-modal
                ref="updateEngagementModal"
                title="Update Engagement"
                size="lg"
                centered>
                <div>
                    <form @submit.prevent="submitUpdateEngagement">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="updateEngagementName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Engagement Name" :state="!$v.updateEngagementName.$invalid"></b-form-input>
                                <!--<p v-if="!$v.projectName.required">The name field is required!</p>-->
                                <!--<p v-if="!$v.projectName.minLength">The name field is minimum 3!</p>-->
                            </b-col>
                        </b-row>
                        <br>
                      <b-row class="my-1">
                            <b-col sm="2"><label class="label">Description:</label></b-col>
                            <b-col sm="10">
                                <b-form-textarea
                                   v-model="updateEngagementDesc"
                                   placeholder="Enter Description"
                                   :rows="3"
                                   :max-rows="6" :state="!$v.updateEngagementDesc.$invalid">
                                </b-form-textarea>
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
                            <b-col sm="2"><label class="label">Start Date:</label></b-col>
                            <b-col sm="10">
                                <date-picker
                                  v-model="updateEngagementDateRange"
                                  range :shortcuts="shortcuts"
                                  format="yyyy-MM-dd"
                                  lang="en" width="100%"
                                  :not-before="today" :state="!$v.updateEngagementDateRange.$invalid"></date-picker>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeUpdateEngagement() "> Close</button>
                        <button type="button"
                                class="btn btn-orange-submit pull-right"
                                data-dismiss="modal"
                                @click=" submitUpdateEngagement() "
                                v-if="!$v.updateEngagementName.$invalid && !$v.updateEngagementDesc.$invalid && !$v.updateApplication.$invalid && !$v.updateEngagementDateRange.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>

        <!--delete-->
        <b-modal ref="deleteEngagementModal" title="Delete Engagement" centered size="lg">
                <div>
                    <form @submit.prevent="submitDeleteEngagement">
                        <p class="delete-header">Are you sure want to delete this engagement ?</p>
                        <br>
                    </form>
                </div>
                <b-col col="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeDeleteEngagement() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitDeleteEngagement() ">
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
    import axios from '@/utils/auth'
    import { required, minLength } from 'vuelidate/lib/validators'
    import DatePicker from 'vue2-datepicker'
    import Loading from 'vue-loading-overlay'
    import 'vue-loading-overlay/dist/vue-loading.min.css'
    import { notValidUser } from '@/utils/checkAuthUser'

    export default {
      name: 'Engagements',
      components: {
        CommonTable,
        DatePicker,
        Loading
      },
      data() {
        return {
          isLoading: false,
          engagementList: [],
          headerTitles: 'List of Engagements',
          individualEngagementUrl: '',
          applicationOption: [],
          engagementName: '',
          engagementDesc: '',
          application: '',
          engagementDateRange: '',
          updateEngagementName: '',
          updateEngagementDesc: '',
          updateApplication: '',
          updateEngagementDateRange: '',
          engagementId: '',
          engagementsCount: 0,
          today: new Date(),
          shortcuts: [
            {
              // text: 'Today',
              start: new Date(),
              end: new Date()
            }
          ]
        }
      },
      validations: {
        engagementName: {
          required,
          minLength: minLength(1)
        },
        engagementDesc: {
          required,
          minLength: minLength(3)
        },
        application: {
          required
        },
        engagementDateRange: {
          required
        },
        updateEngagementName: {
          required,
          minLength: minLength(1)
        },
        updateEngagementDesc: {
          required,
          minLength: minLength(3)
        },
        updateApplication: {
          required
        },
        updateEngagementDateRange: {
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
            this.applicationOption = []
            this.engagementList = []
            this.fetchData()
          })
          this.isLoading = false
        }
      },
      methods: {
        fetchData() {
          if (this.org && this.token) {
            axios.get('/engagements/')
              .then(res => {
                this.engagementsCount = res.data.count
                for (const value of res.data.results) {
                  this.engagementList.push({
                    name: { vul_name: value.name },
                    sev: value.severity,
                    id: value.id,
                    url: 'individual_engagement/' + value.id + '/',
                    appName: value.app_details.name,
                    engId: value.uniq_id
                  })
                }
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
        clickPagination(event) {
          if (event.page) {
            if (event.page > 1) {
              axios.get('/engagements/?page=' + event.page)
                  .then(res => {
                    this.engagementPagnatedList = []
                    for (const value of res.data.results) {
                        this.engagementList.push({
                        name: { vul_name: value.name },
                        sev: value.severity,
                        id: value.id,
                        url: 'individual_engagement/' + value.id + '/',
                        appName: value.app_details.name,
                        engId: value.uniq_id
                  })
                    }
                  }).catch(error => {
                    if (error.response.status === 404) {
                      this.$router.push('/not_found')
                    } else if (error.response.status === 404) {
                      this.$router.push('/forbidden')
                    } else {
                      this.$router.push('/error')
                    }
                  }),
                   axios.get('/applications/')
                  .then(res => {
                    this.applicationOption = []
                    for (const value of res.data) {
                      this.applicationOption.push({ value: value.id, label: value.name })
                    }
                  }).catch(error => {
                    if (error.response.status === 404) {
                      this.$router.push('/not_found')
                    } else if (error.response.status === 404) {
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
        createEngagement() {
          this.$refs.createEngagementModal.show()
          axios.get('/applications/')
            .then(res => {
              for (const value of res.data.results) {
                this.applicationOption.push({ value: value.id, label: value.name })
              }
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 404) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        },
        closeCreateEngagement() {
          this.$refs.createEngagementModal.hide()
        },
        submitCreateEngagement() {
          if (this.org && this.token) {
            const dayOne = new Date(this.engagementDateRange[0])
            const d = dayOne.getDate()
            const m = dayOne.getMonth() + 1
            const y = dayOne.getFullYear()
            const dayTwo = new Date(this.engagementDateRange[1])
            const d1 = dayTwo.getDate()
            const m1 = dayTwo.getMonth() + 1
            const y1 = dayTwo.getFullYear()
            const startDate = y + '-' + (m <= 9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d)
            const stopDate = y1 + '-' + (m1 <= 9 ? '0' + m1 : m1) + '-' + (d1 <= 9 ? '0' + d1 : d1)
            const form_data = new FormData()
            form_data.append('name', this.engagementName)
            form_data.append('description', this.engagementDesc)
            form_data.append('application', this.application.value)
            form_data.append('start_date', startDate)
            form_data.append('stop_date', stopDate)
            axios.put('/engagements/', form_data)
              .then(res => {
                this.$refs.createEngagementModal.hide()
                this.isLoading = true
                this.$notify({
                  group: 'foo',
                  type: 'success',
                  title: 'Engagement',
                  text: 'The Engagement has been created Successfully!',
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
        updateEngagement(event) {
          this.engagementId = event.id
          if (this.org && this.token && this.engagementId) {
            this.$refs.updateEngagementModal.show()
            axios.get('/engagements/' + this.engagementId + '/')
              .then(res => {
                this.updateEngagementName = res.data.name
                this.updateEngagementDesc = res.data.description
                for (const appVal of this.applicationOption) {
                  if (res.data.application === appVal.value) {
                    this.updateApplication = appVal.label
                  }
                }
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 404) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })

            axios.get('/applications/')
              .then(res => {
                for (const value of res.data.results) {
                  this.applicationOption.push({ value: value.id, label: value.name })
                }
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
        closeUpdateEngagement() {
          this.$refs.updateEngagementModal.hide()
        },
        submitUpdateEngagement() {
          if (this.org && this.token && this.engagementId) {
            const dayOne = new Date(this.updateEngagementDateRange[0])
            const d = dayOne.getDate()
            const m = dayOne.getMonth() + 1
            const y = dayOne.getFullYear()
            const dayTwo = new Date(this.updateEngagementDateRange[1])
            const d1 = dayTwo.getDate()
            const m1 = dayTwo.getMonth() + 1
            const y1 = dayTwo.getFullYear()
            const startDate = y + '-' + (m <= 9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d)
            const stopDate = y1 + '-' + (m1 <= 9 ? '0' + m1 : m1) + '-' + (d1 <= 9 ? '0' + d1 : d1)
            const formData = {
              'name': this.updateEngagementName,
              'description': this.updateEngagementDesc,
              'application': this.updateApplication.value,
              'start_date': startDate,
              'stop_date': stopDate
            }
            axios.post('/engagements/' + this.engagementId + '/', formData)
              .then(res => {
                this.$refs.updateEngagementModal.hide()
                this.isLoading = true
                this.$notify({
                  group: 'foo',
                  type: 'info',
                  title: 'Engagement',
                  text: 'The Engagement has been updated Successfully!',
                  position: 'top right'
                })
                this.engagementId = ''
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
        deleteEngagement(event) {
          this.engagementId = event.id
          this.$refs.deleteEngagementModal.show()
        },
        closeDeleteEngagement() {
          this.$refs.deleteEngagementModal.hide()
        },
        submitDeleteEngagement() {
          if (this.org && this.token && this.engagementId) {
            axios.delete('/engagements/' + this.engagementId + '/')
              .then(res => {
                this.$refs.deleteEngagementModal.hide()
                this.isLoading = true
                this.$notify({
                  group: 'foo',
                  type: 'error',
                  title: 'Engagement',
                  text: 'The engagement has been deleted Successfully!',
                  position: 'top right'
                })
                this.engagementId = ''
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
</style>

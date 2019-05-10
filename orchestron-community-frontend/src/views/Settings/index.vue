<template>
    <b-container fluid>
      <loading :active.sync="reloadPage" :can-cancel="true"></loading>
      <common-table :dataItems="orgList" :headerTitle="headerTitles"
            @updateModal="updateOrganization($event)" :pageCount="orgCount" :createButton="createButton" :deleteButton="deleteButton"></common-table>
      <!--Update-->
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
                                <br>
                                <p>Previous logo: {{ updateOrgLogo }} </p>
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
    </b-container>
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
      name: 'Settings',
      components: {
        CommonTable,
        DatePicker,
        Loading
      },
      data() {
        return {
          isLoading: false,
          reloadPage: false,
          orgCount: 0,
          orgList: [],
          headerTitles: 'Organization',
          individualOrgUrl: 'individual_org',
          orgId: '',
          today: new Date(),
          orgName: '',
          updateOrgLogo: '',
          updateOrgLocation: '',
          updateOrgType: '',
          updateOrgTimezone: '',
          updateOrgEndDate: '',
          typeDelete: '',
          orgTimezoneOption: [],
          orgTypeOption: [],
          updateOrgId: '',
          createButton: true,
          deleteButton: true,
          updateOrgName: '',
        }
      },
      validations: {
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
      updated() {
        this.$nextTick(function() {
          if (this.isLoading) {
            this.orgList = []
            this.fetchData()
            this.isLoading = false
          }
        })
      },
      methods: {
        fetchData() {
            this.reloadPage = true
          if (this.org && this.token) {
            axios.get('/organizations/')
              .then(res => {
                this.orgCount = res.data.count
                for (const value of res.data.results) {
                  this.orgList.push({
                    name: { vul_name: value.name },
                    id: value.id, sev: {},
                    url: 'individual_org/' + value.id + '/'
                  })
                }
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
        updateOrganization(event) {
          if (this.org && this.token && event.id) {
            this.updateOrgId = event.id
            this.orgId = this.org
            axios.get('/organizations/' + event.id + '/')
              .then(res => {
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
        closeUpdateOrganization() {
          this.$refs.updateOrgModal.hide()
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
                this.$router.push('/settings/')
                this.updateOrgId = ''
                this.$notify({
                  group: 'foo',
                  type: 'info',
                  title: 'success',
                  text: 'The organization has been updated successfully!',
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
          }else {
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
</style>

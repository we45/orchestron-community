<template>
  <div>
    <b-container fluid>
      <b-card>
        <p class="title">Open Vulnerabilities - {{ selectedOption }} Severity</p>
        <hr>
        <br>
        <b-row>
          <b-col sm="8" class="m2-top">
            <p class="text-left">
              <span class="vul-count">
                {{ totalVul }}
              </span>
            </p>
          </b-col>
          <b-col sm="4">
            <v-select  :options="selectOption"
                       v-model="selectedOption"
                       v-on:input="onInput(selectedOption)">
            </v-select>
          </b-col>
          </b-row>
        <!--<br>-->
        <open-vul-table :pageNumberCount="totalVul"
                        :currentPage="currentPage"
                        :dataItems="items"
                        @updateUncategorized="updateUncategorized($event)"
                        @clickPagination="clickPagination($event)"></open-vul-table>
      </b-card>
           <!--Update Uncategorized-->
      <b-modal ref="UpdateuncategorizedModal" title="Update Uncategorized Vulnerability" size="lg" centered>
              <template>
                <div>
                    <form @submit.prevent="promptUncategorizedUpdateVul">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input v-model="updateUncategorizedVulName" type="text" readonly></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">CWE:</label></b-col>
                            <b-col sm="8">
                              <b-form-input
          id="input-1"
          v-model="updateUncategorizedVulCWE"
          type="number"
          placeholder="Enter CWE"
        ></b-form-input>
                            </b-col>
                          <b-col cols="2">

                          </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeUncategorizedUpdateVul() ">Close</button>
                        <button type="button" class="btn btn-orange-submit pull-right" data-dismiss="modal" @click=" promptUncategorizedUpdateVul() "
                              >
                        Submit
                        </button>
                    </div>
                </b-col>
              </template>
            </b-modal>

      <!--Uncategorized Prompt Modal-->
      <b-modal ref="beforeSubmitUncategorizedModal" title="Update Uncategorized Vulnerability" centered size="lg">
                <div>
                    <form @submit.prevent="submitUncategorizedUpdateVul">
                        <p class="prompt-header">* Vulnerability will be categorized to CWE {{ updateUncategorizedVulCWE }}</p>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" submitUncategorizedUpdateVulClose() ">No</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitUncategorizedUpdateVul() ">
                        Yes
                        </button>
                    </div>
                </b-col>
            </b-modal>
    </b-container>
  </div>
</template>
<script>
import OpenVulTable from '@/components/OpenVulnerabilities/OpenVulTable.vue'
import axios from '@/utils/auth'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'SeverityWise',
  data() {
    return {
      items: [],
      paginationItems: [],
      totalVul: 0,
      highCount: 0,
      mediumCount: 0,
      lowCount: 0,
      infoCount: 0,
      selectOption: ['High', 'Medium', 'Low', 'Info'],
      selectedOption: '',
      isLoading: false,
      currentPage: 0,
      updateUncategorizedVulName: '',
        updateUncategorizedVulCWE: '',
    }
  },
  components: {
    OpenVulTable
  },
  created() {
    this.param = this.$route.params.sev
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
    this.fetchSeverityData()
  },
  updated() {
    if (this.isLoading) {
      this.$nextTick(() => {
        this.items = []
        this.items = this.paginationItems
      })
      this.isLoading = false
    }
  },
  methods: {
    fetchSeverityData() {
      if (this.param === 'high') {
        this.selectedOption = 'High'
      } else if (this.param === 'medium') {
        this.selectedOption = 'Medium'
      } else if (this.param === 'low') {
        this.selectedOption = 'Low'
      } else if (this.param === 'info') {
        this.selectedOption = 'Info'
      } else {
        this.selectedOption = 'Info'
      }
      if (this.org && this.token && this.param) {
        axios.get('/openvul/org/' + this.org + '/?severity=' + this.param)
          .then(res => {
            if (res.status === 200) {
              this.items = []
              this.totalVul = res.data.count
              for (const val of Object.values(res.data.results)) {
                const splitVuls = val.names.split('###,')
                const cwe = val.cwe
                const sev = val.severity
                const openFor = val.open_for
                const tool = val.tools
                let commonName = ''
                let vulName = ''
                let appName = ''
                const multipleVuls = {}
                for (const actualVul of splitVuls) {
                  const vulDetail = actualVul.split('###')
                  vulName = vulDetail[0]
                  appName = vulDetail[1]
                  if (splitVuls.length > 1) {
                    multipleVuls[vulName] = appName
                  }
                }
                if (val.common_name === null) {
                  commonName = vulName
                } else {
                  commonName = val.common_name
                }
                const checkObjectEmpty = Object.keys(multipleVuls).length === 0
                if (checkObjectEmpty) {
                  this.items.push({
                    cwe: cwe,
                    sev: sev,
                    openFor: openFor,
                    commonName: commonName,
                    name: multipleVuls,
                    app: appName,
                    tool: tool,
                    multiple: false,
                    vulName: vulName
                  })
                } else {
                  this.items.push({
                    cwe: cwe,
                    sev: sev,
                    openFor: openFor,
                    commonName: commonName,
                    name: multipleVuls,
                    app: appName,
                    tool: tool,
                    multiple: true,
                    vulName: vulName
                  })
                }
              }
            } else {
              this.$router.push('/forbidden')
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
    onInput(value) {
      this.param = ''
      if (value === 'High') {
        this.param = 'high'
      } else if (value === 'Medium') {
        this.param = 'medium'
      } else if (value === 'Low') {
        this.param = 'low'
      } else if (value === 'Info') {
        this.param = 'info'
      } else {
        this.param = 'info'
      }
      if (this.org && this.token && this.param) {
        axios.get('/openvul/org/' + this.org + '/?severity=' + this.param)
          .then(res => {
            if (res.status === 200) {
              this.items = []
              this.totalVul = 0
              this.highCount = 0
              this.mediumCount = 0
              this.lowCount = 0
              this.infoCount = 0
              this.totalVul = res.data.count
              for (const val of Object.values(res.data.results)) {
                const splitVuls = val.names.split('###,')
                const cwe = val.cwe
                const sev = val.severity
                const openFor = val.open_for
                const tool = val.tools
                var commonName = ''
                var vulName = ''
                var appName = ''
                const multipleVuls = {}
                for (const actualVul of splitVuls) {
                  const vulDetail = actualVul.split('###')
                  vulName = vulDetail[0]
                  appName = vulDetail[1]
                  if (splitVuls.length > 1) {
                    multipleVuls[vulName] = appName
                  }
                }
                if (val.common_name === null) {
                  commonName = vulName
                } else {
                  commonName = val.common_name
                }
                const checkObjectEmpty = Object.keys(multipleVuls).length === 0
                if (checkObjectEmpty) {
                  this.items.push({
                    cwe: cwe,
                    sev: sev,
                    openFor: openFor,
                    commonName: commonName,
                    name: multipleVuls,
                    app: appName,
                    tool: tool,
                    multiple: false,
                    vulName: vulName
                  })
                } else {
                  this.items.push({
                    cwe: cwe,
                    sev: sev,
                    openFor: openFor,
                    commonName: commonName,
                    name: multipleVuls,
                    app: appName,
                    tool: tool,
                    multiple: true,
                    vulName: vulName
                  })
                }
              }
            } else {
              this.$router.push('/forbidden')
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
        this.currentPage = event.page
        this.isLoading = true
        if (this.currentPage > 1) {
          if (this.org && this.token && this.param) {
            axios.get('/openvul/org/' + this.org + '/?severity='+ this.param + '&page=' + event.page)
              .then(res => {
                if (res.status === 200) {
                  this.items = []
                  this.paginationItems = []
                  this.isLoading = true
                  for (const val of Object.values(res.data.results)) {
                    const splitVuls = val.names.split('###,')
                    const cwe = val.cwe
                    const sev = val.severity
                    const openFor = val.open_for
                    const tool = val.tools
                    let commonName = ''
                    let vulName = ''
                    let appName = ''
                    const multipleVuls = {}
                    for (const actualVul of splitVuls) {
                      const vulDetail = actualVul.split('###')
                      vulName = vulDetail[0]
                      appName = vulDetail[1]
                      if (splitVuls.length > 1) {
                        multipleVuls[vulName] = appName
                      }
                    }
                    if (val.common_name === null) {
                      commonName = vulName
                    } else {
                      commonName = val.common_name
                    }
                    const checkObjectEmpty = Object.keys(multipleVuls).length === 0
                    if (checkObjectEmpty) {
                      this.paginationItems.push({
                        cwe: cwe,
                        sev: sev,
                        openFor: openFor,
                        commonName: commonName,
                        name: multipleVuls,
                        app: appName,
                        tool: tool,
                        multiple: false,
                        vulName: vulName
                      })
                    } else {
                      this.paginationItems.push({
                        cwe: cwe,
                        sev: sev,
                        openFor: openFor,
                        commonName: commonName,
                        name: multipleVuls,
                        app: appName,
                        tool: tool,
                        multiple: true,
                        vulName: vulName
                      })
                    }
                  }
                } else {
                  this.$router.push('/forbidden')
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
        } else {
          this.fetchSeverityData()
        }
      }
    },
    updateUncategorized(event) {
      this.updateUncategorizedVulName = ''
      this.updateUncategorizedVulName = event.commonName
      this.$refs.UpdateuncategorizedModal.show()
    },
      closeUncategorizedUpdateVul() {
      this.$refs.UpdateuncategorizedModal.hide()
    },
    promptUncategorizedUpdateVul() {
      this.$refs.beforeSubmitUncategorizedModal.show()
    },
    submitUncategorizedUpdateVulClose() {
      this.$refs.beforeSubmitUncategorizedModal.hide()
    },
    submitUncategorizedUpdateVul() {
      this.$refs.beforeSubmitUncategorizedModal.hide()
      this.$refs.UpdateuncategorizedModal.hide()

      const formData = {
        'common_name': this.updateUncategorizedVulName,
        'cwe': this.updateUncategorizedVulCWE,
        'name': this.updateUncategorizedVulName
      }

      axios.post('/openvul/catgorize/', formData)
        .then(res => {
          this.$refs.beforeSubmitUncategorizedModal.hide()
          this.$refs.UpdateuncategorizedModal.hide()
          this.isLoading = true
          this.$notify({
            group: 'foo',
            type: 'info',
            title: 'success',
            text: 'The vulnerability has been updated successfully!',
            position: 'top right'
          })
          this.$router.go()
        }).catch(error => {
          if (error.response.data.detail === 'Signature has expired.'){
                  notValidUser()
                  this.$router.push('/')
                }
        })

      // openvul/catgorize
    },
  }
}
</script>
<style scoped>
  .vul-count{
    font-family: 'Avenir';
    color: #25231F;
    font-size: 48px;
    font-weight: 200;
    line-height: 0.33;
  }
  .btn-orange-close {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
    /*height: 20px;*/

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

  .prompt-header {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 500;
    line-height: 0.99;
    text-align: center;
    color: #232325;
  }
</style>

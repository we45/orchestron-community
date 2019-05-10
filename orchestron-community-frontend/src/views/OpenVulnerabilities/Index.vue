<template>
  <div>
    <b-container fluid>
      <loading :active.sync="reloadPage" :can-cancel="true"></loading>
      <b-card>
        <p>{{ headerTitle }}</p>
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
            <v-select :options="selectOption"
                      v-model="selectedOption"
                      v-on:input="onInput(selectedOption)">
            </v-select>
          </b-col>
        </b-row>
        <br>
        <vul-progress-bar
          :high="highCount"
          :medium="mediumCount"
          :low="lowCount"
          :info="infoCount"
          :total="totalVul"></vul-progress-bar>
        <br>
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
  import OpenVulTableDash from '@/components/OpenVulnerabilities/OpenVulTableDashboard.vue'
  import VulProgressBar from '@/components/OpenVulnerabilities/VulProgressBar'
  import axios from '@/utils/auth'
  import {notValidUser} from '@/utils/checkAuthUser'
  import Loading from 'vue-loading-overlay'

  export default {
    name: 'OpenVulnerabilities',
    components: {
      OpenVulTable,
      VulProgressBar,
      OpenVulTableDash,
      Loading
    },
    data() {
      return {
        headerTitle: '',
        items: [],
        reloadPage: false,
        paginationItems: [],
        totalVul: 0,
        highCount: 0,
        mediumCount: 0,
        lowCount: 0,
        infoCount: 0,
        selectOption: ['Default View', 'Show False Positives'],
        selectedOption: 'Default View',
        isLoading: false,
        currentPage: 0,
        checkAppNames: [],
        updateUncategorizedVulName: '',
        updateUncategorizedVulCWE: '',
      }
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
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
      checkAppExists(val) {
        return this.checkAppNames.some(function (el) {
          return el.value !== val;
        });
      },
      fetchFalsePositiveData() {
        if (this.org && this.token) {
          var url = '/openvul/org/' + this.org + '/?false=1'
          axios.get(url)
            .then(res => {
              this.headerTitle = 'Open Vulnerabilities'
              this.items = []
              this.paginationItems = []
              this.totalVul = 0
              this.totalVul = res.data.count
              this.highCount = res.data.severity[3] | 0
              this.mediumCount = res.data.severity[2] | 0
              this.lowCount = res.data.severity[1] | 0
              this.infoCount = res.data.severity[0] | 0

              for (const val of res.data.results) {
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
                    // multipleVuls[vulName] = appName
                    multipleVuls[vulName+'!!!###!!!'+appName] = appName
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
      fetchData() {
        this.isLoading = true
        if (this.org && this.token) {
          var url = '/openvul/org/' + this.org + '/?true=1'
          axios.get(url)
            .then(res => {
              this.headerTitle = 'Open Vulnerabilities'
              this.items = []
              this.paginationItems = []
              this.totalVul = 0
              this.totalVul = res.data.count
              this.highCount = res.data.severity[3] | 0
              this.mediumCount = res.data.severity[2] | 0
              this.lowCount = res.data.severity[1] | 0
              this.infoCount = res.data.severity[0] | 0

              for (const val of res.data.results) {
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
                     multipleVuls[vulName+'!!!###!!!'+appName] = appName
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
        }else {
          notValidUser()
          this.$router.push('/')
        }
      },
      clickPagination(event) {
        if(this.org && this.token) {
          if (event.page) {
            this.reloadPage = true
            this.currentPage = event.page
            if (this.currentPage > 1) {
              if (this.selectedOption == 'Default View') {
                var url = '/openvul/org/' + this.org + '/?true=1&page=' + event.page
              }
              else {
                var url = '/openvul/org/' + this.org + '/?false=1&page=' + event.page
              }
              axios.get(url)
                .then(res => {
                  this.headerTitle = 'Open Vulnerabilities'
                  this.isLoading = true
                  this.totalVul = 0
                  this.items = []
                  this.paginationItems = []
                  this.totalVul = res.data.count
                  this.highCount = 0
                  this.mediumCount = 0
                  this.lowCount = 0
                  this.infoCount = 0
                  this.highCount = res.data.severity[3] | 0
                  this.mediumCount = res.data.severity[2] | 0
                  this.lowCount = res.data.severity[1] | 0
                  this.infoCount = res.data.severity[0] | 0
                  for (const val of res.data.results) {
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
                        // multipleVuls[vulName] = appName
                        multipleVuls[vulName+'!!!###!!!'+appName] = appName
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
                  this.reloadPage = false

                }).catch(error => {
                this.reloadPage = false

                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 404) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })
            } else {
              this.fetchData()
            }
          }
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
      onInput(value) {
        if (value === 'Default View' || value === null) {
          this.fetchData()
        } else {
          this.fetchFalsePositiveData()
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
  .vul-count {
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

<template>
  <div>
    <b-container fluid>
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

            <v-select  :options="selectOption"
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
                        @clickPagination="clickPagination($event)"></open-vul-table>
      </b-card>
    </b-container>
  </div>
</template>
<script>
import OpenVulTable from '@/components/OpenVulnerabilities/OpenVulTable.vue'
import VulProgressBar from '@/components/OpenVulnerabilities/VulProgressBar'
import axios from '@/utils/auth'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'OpenVulnerabilities',
  components: {
    OpenVulTable,
    VulProgressBar
  },
  data() {
    return {
      headerTitle: '',
      items: [],
      paginationItems: [],
      totalVul: 0,
      highCount: 0,
      mediumCount: 0,
      lowCount: 0,
      infoCount: 0,
      selectOption: ['Default View', 'Show False Positives'],
      selectedOption: 'Default View',
      isLoading: false,
      currentPage: 0
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
        this.items = []
        this.items = this.paginationItems
      })
      this.isLoading = false
    }
  },
  methods: {
    fetchData() {
      if (this.org && this.token) {
        if(this.selectedOption == 'Default View'){
          var url ='/openvul/org/' + this.org + '/?true=1'
        }
        else{
          var url = '/openvul/org/' + this.org + '/?false=1'
        }
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
              const splitVuls = val.names.split(',')
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
                if (splitVuls.length > 2) {
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
        this.currentPage = event.page
        if (this.currentPage > 1) {
             if(this.selectedOption == 'Default View'){
          var url ='/openvul/org/' + this.org + '/?true=1&page=' + event.page
        }
        else{
          var url = '/openvul/org/' + this.org + '/?false=1&page='  + event.page
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
                const splitVuls = val.names.split(',')
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
                  if (splitVuls.length > 2) {
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
          this.fetchData()
        }
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    onInput(value) {
      if (value === 'Default View' || value === null) {
        if (this.org && this.token) {
          axios.get('/openvul/org/' + this.org + '/?true=1&page=1')
            .then(res => {
              this.headerTitle = 'Open Vulnerabilities'
              this.items = []
              this.totalVul = 0
              this.highCount = 0
              this.mediumCount = 0
              this.lowCount = 0
              this.infoCount = 0
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
                const splitVuls = val.names.split(',')
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
                  if (splitVuls.length > 2) {
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
        if (this.org && this.token) {
          axios.get('/openvul/org/' + this.org + '/?false=1')
            .then(res => {
              this.headerTitle = 'False Positives'
              this.items = []
              this.totalVul = 0
              this.highCount = 0
              this.mediumCount = 0
              this.lowCount = 0
              this.infoCount = 0
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
                const splitVuls = val.names.split(',')
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
                  if (splitVuls.length > 2) {
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
</style>

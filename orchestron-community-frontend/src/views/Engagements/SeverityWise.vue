<template>
    <div>
        <b-container fluid>
            <b-card>
                <p class="title">Open Vulnerabilities by {{ selectedOption }} Severity</p>
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
                <!-- <open-vul-table :dataItems="items"
                ></open-vul-table> -->
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
import axios from '@/utils/auth'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'EngagementSeverityWise',
  data() {
    return {
      items: [],
      totalVul: 0,
      highCount: 0,
      mediumCount: 0,
      lowCount: 0,
      infoCount: 0,
      selectOption: ['High', 'Medium', 'Low', 'Info'],
      selectedOption: '',
      currentPage: 0
    }
  },
  components: {
    OpenVulTable
  },
  created() {
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
    this.param = this.$route.params.sev
    this.engId = this.$route.params.engagementId
    this.fetchSeverityData()
  },
  methods: {
    fetchSeverityData() {
      if (this.org && this.token) {
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
        axios.get('/openvul/engagement/' + this.engId + '/?severity=' + this.param)
          .then(res => {
            // if (res.status === 200) {
              this.items = []
              this.totalVul = res.data.count

              for (const val of Object.values(res.data.results)) {
                const splitVuls = val.names.split('###,')
                const cwe = val.cwe
                const sev = val.severity
                const openFor = val.aging
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
            // } else {
            //   this.$router.push('/forbidden')
            // }
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
       if (this.org && this.token) {
      if (event.page) {
        this.currentPage = event.page
        if (this.currentPage > 1) {
          axios.get('/openvul/engagement/' + this.engId + '/?severity=' + this.param+'&page='+event.page)
          .then(res => {
            // if (res.status === 200) {
              this.items = []
              for (const val of Object.values(res.data.results)) {
                const splitVuls = val.names.split('###,')
                const cwe = val.cwe
                const sev = val.severity
                const openFor = val.aging
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
          this.fetchSeverityData()
        }
      } else {
        this.fetchSeverityData()
      }
      } else {
        notValidUser()
        this.$router.push('/')
      }
    },
    onInput(value) {
      if (this.org && this.token) {
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

        axios.get('/openvul/engagement/' + this.engId + '/?severity=' + this.param)
          .then(res => {
            // if (res.status === 200) {
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
                const openFor = val.aging
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

            // } else {
            //   this.$router.push('/forbidden')
            // }
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

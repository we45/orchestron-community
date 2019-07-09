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
        <sev-table :dataItems="sevData"></sev-table>
      </b-card>
    </b-container>
  </div>
</template>
<script>
import SevTable from '@/components/Scans/SevTable.vue'
import axios from '@/utils/auth'
import { notValidUser } from '@/utils/checkAuthUser'

export default {
  name: 'ScanSeverityWise',
  data() {
    return {
      sevData: [],
      totalVul: 0,
      selectOption: ['High', 'Medium', 'Low', 'Info'],
      selectedOption: '',
      appId: ''
    }
  },
  components: {
    SevTable
  },
  created() {
    this.param = this.$route.params.sev
    this.scanId = this.$route.params.scanId
    this.org = localStorage.getItem('org')
    this.token = localStorage.getItem('token')
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
        axios.get('/scans/' + this.scanId + '/?severity=' + this.param)
          .then(res => {
            this.appId = res.data.application
            this.sevData = []
            for (const vul of res.data.vuls) {
              for (const val of Object.values(vul)) {
                this.sevData.push({
                  sev: val.severity,
                  name: val.name,
                  cwe: val.cwe,
                  id: val.id,
                  url: '/projects/individual_application/' + this.appId + '/individual_scan/' + this.scanId + '/individual_vul/' + val.id + '/'
                  
                })
              }
            }
            this.totalVul = res.data.vuls.length
          }).catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
              notValidUser()
              this.$router.push('/')
            }
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
        axios.get('/scans/' + this.scanId + '/?severity=' + this.param)
          .then(res => {
            
            this.sevData = []
            this.totalVul = 0
            this.totalVul = res.data.vuls.length
            for (const vul of res.data.vuls) {
              for (const val of Object.values(vul)) {
                this.sevData.push({
                  sev: val.severity,
                  name: val.name,
                  cwe: val.cwe,
                  id: val.id,
                  // url: this.scanId + '/individual_vul/' + val.id
                   url: '/projects/individual_application/' + this.appId + '/individual_scan/' + this.scanId + '/individual_vul/' + val.id + '/'
                })
              }
            }
            
          }).catch(error => {
            if (error.response.data.detail === 'Signature has expired.'){
              notValidUser()
              this.$router.push('/')
            }
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
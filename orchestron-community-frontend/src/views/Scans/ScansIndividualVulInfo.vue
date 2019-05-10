<template>
  <div>
    <b-row>
      <b-col cols="4"></b-col>
      <b-col cols="6">
            <button-groups :markTruePositive="markTruePositive"
                    :fixVulnerability="fixVulnerability"
                    :updateVul="updateVul"
                    :raiseBug="raiseBug" :markFalsePositive="markFalsePositive"></button-groups>
      </b-col>
      <b-col cols="2"></b-col>
    </b-row>
    <br/>
    <b-container fluid>
      <b-card>
        <b-row>
          <b-col cols="8">
            <p class="vul-name">{{ vulName }}</p>
          </b-col>
          <b-col cols="3">
          </b-col>
            <b-col cols="1">
            <span size="sm" class="high" v-if="sev===3">High</span>
            <span size="sm" class="medium" v-if="sev===2">Medium</span>
            <span size="sm" class="low" v-if="sev===1">Low</span>
            <span size="sm" class="info" v-if="sev===0">Info</span>
          </b-col>
        </b-row>
        <b-tabs pills card v-if="basicInfo.length > 0 || vulInfo.length > 0 || affectedInstances.length > 0">
          <b-tab title="Basic Info" active v-if="basicInfo.length > 0">
            <basic-info :basicInfoData="basicInfo"></basic-info>
          </b-tab>
          <b-tab title="Vulnerability Info" v-if="vulInfo.length > 0 && vulInfo[0].desc">
            <vulnerability-info :vulInfo="vulInfo"></vulnerability-info>
          </b-tab>
          <b-tab title="Affected Instances" v-if="affectedInstances.length > 0">
            <affected-instances :affectedInstances="affectedInstances"></affected-instances>
          </b-tab>
        </b-tabs>
      </b-card>
    </b-container>
  </div>
</template>

<script>
  import BasicInfo from '@/components/IndividualVulnerability/BasicInfo'
  import VulnerabilityInfo from '@/components/IndividualVulnerability/VulnerabilityInfo'
  import AffectedInstances from '@/components/IndividualVulnerability/AffectedInstances'
  import ButtonGroups from '@/components/IndividualVulnerability/ButtonGroups'
  import axios from '@/utils/auth'
  import { notValidUser } from '@/utils/checkAuthUser'

  export default {
    name: 'ScansIndividualVulInfo',
    data() {
      return {
        vulName: '',
        sev: '',
        basicInfo: [],
        vulInfo: [],
        affectedInstances:[],
        markTruePositive: false,
        markFalsePositive: false,
        fixVulnerability: false,
        updateVul: false,
        raiseBug: false
      }
    },
    components: {
      ButtonGroups,
      BasicInfo,
      VulnerabilityInfo,
      AffectedInstances
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.vulId = this.$route.params.vulId
      this.fetchData()
    },
    methods: {
      fetchData() {
        if (this.org && this.token) {
          axios.get('/vulnerabilities/' + this.vulId + '/')
            .then(res => {
             
              this.sev = res.data.severity
              this.vulName = res.data.name
              let tools = []
              tools.push(res.data.tool)
              this.basicInfo.push({
                'appName': res.data.app_details.name,
                'appUrl': res.data.app_details.url,
                'tool': tools,
                'owasp': res.data.owasp,
                'cwe': res.data.cwe,
                'openFor': null,
                'languages': [],
                'bugStatus': res.data.jira_issue_status,
                'bugId': res.data.jira_id,
                'dread': null,
                'dreadValues': 'Damage: ' + 0 + '\n' + 'Reproducibility: ' + 0 +
                '\n' + 'Exploitability: ' + 0 + '\n' + 'Affected Users: ' + 0 +
                '\n' + 'Discoverability: ' + 0
              })
              // this.basicInfo.push({
              //   'appName': 'appName',
              //   'appUrl': 'AppURL',
              //   'tool': tools,
              //   'owasp': res.data.owasp,
              //   'cwe': res.data.cwe,
              //   'openFor': null,
              //   'languages': [],
              //   'bugStatus': 'BUG Status',
              //   'bugId': 'Bug ID',
              //   'dread': null,
              //   'dreadValues': 'Damage: ' + 0 + '\n' + 'Reproducibility: ' + 0 +
              //   '\n' + 'Exploitability: ' + 0 + '\n' + 'Affected Users: ' + 0 +
              //   '\n' + 'Discoverability: ' + 0
              // })
              this.vulInfo.push({
                desc: res.data.description
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
      }
    }
  }
</script>

<style scoped>
.vul-name {
    font-family: 'Avenir';
    font-size: 14px;
    font-weight: 600;
    line-height: 0.99;
    text-align: left;
    color: #232328;
}
  .high {
    display: inline-block;
    min-width: 35px;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.75;
    color: #FFFFFF;
    text-align: center;
    font-family: 'Avenir';
    white-space: nowrap;
    vertical-align: middle;
    background-color: #d11d55;
    height: 25px;
    margin-right: 3%;
}
.medium {
    display: inline-block;
    min-width: 35px;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.75;
    color: #FFFFFF;
    text-align: center;
    font-family: 'Avenir';
    white-space: nowrap;
    vertical-align: middle;
    background-color: #ff9c2c;
    height: 25px;
    margin-right: 3%;
}
.low {
    display: inline-block;
    min-width: 35px;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.75;
    color: #FFFFFF;
    text-align: center;
    font-family: 'Avenir';
    white-space: nowrap;
    vertical-align: middle;
    background-color: #008b8f;
    height: 25px;
    margin-right: 3%;
}
.info {
    display: inline-block;
    min-width: 35px;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.75;
    color: #FFFFFF;
    text-align: center;
    font-family: 'Avenir';
    white-space: nowrap;
    vertical-align: middle;
    background-color: #1d1e52;
    height: 25px;
    margin-right: 3%;
}
</style>

<template>
    <div>
      <b-row>
        <b-col cols="12" xs="12">
      <b-pagination size="md"
                      :total-rows="excutiveNoPages"
                      v-model="currentPage" :per-page="5"
                      @input="paginationClick(currentPage)" style="float: right;" >
        </b-pagination>
          </b-col>
        </b-row>
      <br>
      <br>
      <template v-if="excutiveVulDataItems.length > 0">
      <template v-for="vuls,index in excutiveVulDataItems">
    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-btn block href="#" v-b-toggle="'vul-'+index"
                style="text-align: left;font-size: 16px;background-color: #F2F2F2;color: #000000;border: none;"
               >
          {{ vuls.vulnerability }}

          <b-badge class="high" v-if="vuls.severity===3">{{ highLable }}</b-badge>
          <b-badge class="medium" v-if="vuls.severity===2">{{ mediumLable }}</b-badge>
          <b-badge class="low" v-if="vuls.severity===1">{{ lowLable }}</b-badge>
          <b-badge class="info" v-if="vuls.severity===0">{{ infoLable }}</b-badge>
        </b-btn>
      </b-card-header>
      <b-collapse :id="'vul-'+index" visible accordion="Vulnerability" role="tabpanel">
        <b-card-body>
          <b-row>
            <b-col cols="6">
              <p class="text-left">
                  <span class="label-name">Application</span>
                  <span class="label-divider">:</span>
                  <span class="label-value">{{ vuls.application }}</span>
              </p>
              <p class="text-left">
                  <span class="label-name">CWE</span>
                  <span class="label-divider">:</span>
                  <span class="label-value">{{ vuls.cwe }}</span>
              </p>
            </b-col>
          
          </b-row>
          
          <br>
         
          <br>
          <br>
        </b-card-body>
      </b-collapse>
    </b-card>
      </template>
        </template>
    </div>
</template>

<script>
  import axios from '@/utils/auth'
  import { notValidUser } from '@/utils/checkAuthUser'
  export default {
    name: 'excutiveVulInfo',
    props: {
      excutiveVulDataItems: {
        type: Array,
        required: true
      },
      excutiveNoPages: {
        required: true
      }
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.fetchSeverityLabel()
    },
    data() {
      return {
        highLable: 'High',
        mediumLable: 'Medium',
        lowLable: 'Low',
        infoLable: 'Info',
        currentPage: 1
      }
    },
    methods: {
      paginationClick(currentPage) {
        this.$emit('clickPagination', { page: currentPage })
      }
    }
  }
</script>

<style scoped>

.high {
  background-color: #d11d55;
  color: #EEEEEE;
  font-size: 14px;
  float: right;
  font-family: Avenir;
}
.medium {
  background-color: #ff9c2c;
  color: #EEEEEE;
  font-size: 14px;
  float: right;
  font-family: Avenir;
}
.low {
  background-color: #008b8f;
  color: #EEEEEE;
  font-size: 14px;
  float: right;
  font-family: Avenir;
}
.info {
  background-color: #1d1e52;
  color: #EEEEEE;
  font-size: 14px;
  float: right;
  font-family: Avenir;
}
</style>

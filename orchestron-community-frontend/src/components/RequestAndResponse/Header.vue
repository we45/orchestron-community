<template>
    <b-container fluid style="background-color: #FFFFFF;">
      <br>
      <template v-for="reqResp in reqResHeaderData ">
        <p> <strong> {{ reqResp.url | decode }} </strong></p>
        <hr>
        <b-row>
          <b-col cols="6">
            <p> <span class="app-created-on">Application</span>  <span class="app-divider">:</span> <strong class="app-value">{{ reqResp.appName }}</strong></p>
            <p> <span class="app-created-on">CWE</span>  <span class="app-divider">:</span> <span class="app-value">{{ reqResp.cwe }}</span></p>
            <p> <span class="app-created-on">Tool</span>  <span class="app-divider">:</span> <span class="app-value">{{ reqResp.tool }}</span></p>
          </b-col>
          <b-col cols="6">
            <p> <span class="app-created-on">OWASP</span>  <span class="app-divider">:</span> <span class="app-value">{{ reqResp.owasp }}</span></p>
            <p> <span class="app-created-on">Scan Name</span>  <span class="app-divider">:</span> <span class="app-value">{{ reqResp.scanName }}</span></p>
          </b-col>
        </b-row>
      </template>
    </b-container>
</template>

<script>
    export default {
      name: 'ReqRespHeader',
      props: {
        reqResHeaderData: {
          type: Array,
          required: true
        }
      }
    }
</script>

<style scoped>
  .app-created-on {
    color: #979797;
    font-family: 'Avenir';
    font-size: 13px;
    font-weight: 600;
    line-height: 1.5;
    text-align: left;
    display: inline-block;
    width: 130px;
    padding-left: 3%;
  }

  .app-value {
    color: #232328;
    font-family: 'Avenir';
    font-size: 13px;
    width: 200px;
    text-align: left;
    display: inline-block;
  }

  .app-divider {
    color: #979797;
    font-family: 'Avenir';
    font-size: 14px;
    font-weight: 600;
    line-height: 1.5;
    text-align: center;
    display: inline-block;
    width: 5px;
  }
</style>

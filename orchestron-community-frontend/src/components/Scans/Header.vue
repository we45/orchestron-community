<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <b-row>
                <template v-for="scan in scanHeader">
                    <b-col cols="4">
                        <p class="wordwrap">
                            <span class="app-created-on">Scan Created by</span>
                            <span class="app-divider">:</span>
                            <strong class="app-value">{{ scan.scanCreatedBy }}</strong>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Application</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ scan.appName }}</span>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Scan Name</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ scan.name }}</span>
                        </p>
                    </b-col>
                    <b-col cols="4">
                        <p class="wordwrap">
                            <span class="app-created-on">Tool</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ scan.tool }}</span>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Scan Date</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ scan.date | moment("MMMM Do YYYY") }}</span>
                        </p>
                    </b-col>
                    <b-col cols="4">
                        <b-btn @click="addVulnerabilities" class="btn-orange">Manual - Add Vulnerability</b-btn>
                    </b-col>
                </template>
            </b-row>
            <br>
        </b-container>
    </div>
</template>

<script>
    export default {
      name: 'ScanHeader',
      props: {
        scanHeader: {
          type: Array,
          required: false
        }
      },
      data() {
        return {
          showModal: true
        }
      },
      methods: {
        addVulnerabilities() {
          this.$emit('addVulnerabilities', {show: this.showModal })
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

  .btn-orange {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:focus,
  .btn-orange.focus {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }
</style>

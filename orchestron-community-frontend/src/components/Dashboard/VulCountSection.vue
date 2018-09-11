<template>
    <div>
        <b-container fluid>
            <b-row style="background-color: #FFFFFF;">
                <b-col v-if="openVul >0 ">
                    <center>
                        <br/>
                        <p class="title">Open Vulnerabilities</p>
                        <br>
                        <router-link :to="openVulUrl">
                            <p>
                                
                                <strong class="open-vul-count">
                                {{ openVul }}
                                </strong>
                            </p>
                        </router-link>
                    </center>
                </b-col>
                <b-col v-else>
                    <center>
                        <br/>
                        <p class="title">Open Vulnerabilities</p>
                        <br>
                        <p>
                            
                            <strong class="open-vul-count">
                            {{ openVul }}
                            </strong>
                        </p>
                    </center>
                </b-col>
                <b-col v-if="closedVul > 0">
                    <center>
                        <br/>
                        <p class="title">Closed Vulnerabilities</p>
                        <br>
                        <router-link :to="closedVulUrl">
                            <p>
                                <strong class="closed-vul-count">
                                {{ closedVul }}
                                </strong>
                            </p>
                        </router-link>
                    </center>
                </b-col>
                <b-col v-else>
                    <center>
                        <br/>
                        <p class="title">Closed Vulnerabilities</p>
                        <br>
                            <p>
                                <strong class="closed-vul-count">
                                {{ closedVul }}
                                </strong>
                            </p>
                    </center>
                </b-col>
                <b-col>
                    <center>
                        <br/>
                        <p class="title">Avg Days Vul Open</p>
                        <br>
                        <p class="org-grade-no-data">{{ grade }}</p>
                    </center>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
      name: 'VulCountSection',
      props: {
        openVul: {
          type: Number,
          required: true
        },
        closedVul: {
          type: Number,
          required: true
        },
        grade: {
          required: true
        },
        openVulUrl: {
          type: String,
          required: true
        },
        closedVulUrl: {
          type: String,
          required: true
        }
      }
    }
</script>

<style scoped>
  .title {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }

  .open-vul-count {
    font-family: 'Avenir';
    color: #FF4C4C;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .closed-vul-count {
    font-family: 'Avenir';
    color: #00AB69;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .org-grade-no-data {
    font-family: 'Avenir';
    color: #d11d55;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }
</style>

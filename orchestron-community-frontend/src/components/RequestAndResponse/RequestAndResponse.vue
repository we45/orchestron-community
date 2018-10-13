<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <b-row>
                <b-col>
                    <b-tabs>
                        <b-tab title="Request" active v-if="req_res_log['req_status']">
                            <br>
                            <template>
                              <div class="code-background">
                                {{ req_res_log['req'] | decode | decode }}
                              </div>
                            </template>
                        </b-tab>
                        <b-tab title="Response" v-if="req_res_log['res_status']">
                            <br>
                          <template>
                            <div class="code-background">
                              {{ req_res_log['res'] | decode | decode }}
                            </div>
                          </template>
                        </b-tab>
                      <b-tab title="Log" v-if="req_res_log['log_status']">
                            <br>
                          <template>
                            <div style="background-color: #2b2b2b; color: #ffb648;font-family: Monaco;margin: 2%;border-radius: 5px;padding: 2%;">
                              {{ req_res_log['log'] | decode }}
                              
                            </div>
                          </template>
                        </b-tab>
                    </b-tabs>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
      name: 'RequestAndResponse',
      props: {
        reqRespData: {
          type: Array,
          required: false
        },
        request: {
          type: Boolean,
          required: false
        },
        response: {
          type: Boolean,
          required: false
        },
        log: {
          type: Boolean,
          required: false
        },
        req_res_log:{
          required:true
        },
      }
    }
</script>

<style scoped>
  .code-background {
    background-color: #dedede;
    border: 2px solid #404042;
    word-wrap: break-word;
    -ms-word-wrap: break-word;
    margin: 0.8em 0;
    padding: 5px;
    font-size: 0.8em;
    max-height: 700px;
    overflow-y: auto;
  }
</style>
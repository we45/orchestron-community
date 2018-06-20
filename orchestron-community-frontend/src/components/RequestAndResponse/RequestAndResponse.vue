<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <b-row>
                <b-col>
                    <b-tabs>
                        <b-tab title="Request" active v-if="request">
                            <br>
                            <template v-for="req in reqRespData">
                              <div class="code-background">
                                {{ req.request | decode | decode }}
                              </div>
                            </template>
                        </b-tab>
                        <b-tab title="Response" v-if="response">
                            <br>
                          <template v-for="req in reqRespData">
                            <div class="code-background">
                              {{ req.response | decode | decode }}
                            </div>
                          </template>
                        </b-tab>
                      <b-tab title="Log" v-if="log">
                            <br>
                          <template v-for="req in reqRespData">
                            <div style="background-color: #2b2b2b; color: #ffb648;font-family: Monaco;margin: 2%;border-radius: 5px;padding: 2%;">
                              {{ req.log | decode }}
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
        }
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

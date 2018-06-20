<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <b-row>
                <template v-for="engagement in engagementHeader">
                    <b-col cols="6">
                        <p class="wordwrap">
                            <span class="app-created-on">Name</span>
                            <span class="app-divider">:</span>
                            <strong class="app-value">{{ engagement.name }}</strong>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Application</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.appName }}</span>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Description</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.desc }}</span>
                        </p>
                      <p class="wordwrap" v-if="engagement.closedBy">
                            <span class="app-created-on">Closed By</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.closedBy }}</span>
                        </p>
                    </b-col>
                    <b-col cols="6">
                        <p class="wordwrap">
                            <span class="app-created-on">Start Date</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.startDate | moment("MMMM Do YYYY") }}</span>
                        </p>
                        <p class="wordwrap">
                            <span class="app-created-on">Stop Date</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.stopDate | moment("MMMM Do YYYY") }}</span>
                        </p>
                      <p class="wordwrap" v-if="engagement.closedDate">
                            <span class="app-created-on">Closed Date</span>
                            <span class="app-divider">:</span>
                            <span class="app-value">{{ engagement.closedDate | moment("MMMM Do YYYY") }}</span>
                        </p>
                    </b-col>
                </template>
            </b-row>
            <br>
        </b-container>
    </div>
</template>

<script>
    export default {
      name: 'EngagementHeader',
      props: {
        engagementHeader: {
          type: Array,
          required: false
        }
      },
      data() {
        return {
          showReport: false
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

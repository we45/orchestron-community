<template>
    <div>
    <b-container fluid style="background-color: #FFFFFF;">
      <br>
      <b-row>
        <b-col cols="2">
          <img :src="'data:image/png;base64,' + logo" style="height: 120px; width: 120px;" >
        </b-col>
        <b-col cols="10">
          <b-row>
            <b-col cols="6">
              <p class="wordwrap">
                <span class="app-created-on">Project</span>
                <span class="app-divider">:</span>
                <strong class="app-value">{{ name }}</strong>
              </p>
               <p class="wordwrap">
                 <span class="app-created-on">Created on</span>
                 <span class="app-divider">:</span>
                 <span class="app-value">{{ createdOn | moment("MMMM Do YYYY")}}</span>
               </p>
            </b-col>
            <b-col cols="6">
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <br>

    </b-container>
  </div>
</template>

<script>
    export default {
      name: 'Headers',
      props: {
        name: {
          type: String,
          required: true
        },
        createdOn: {
          required: true
        },
        logo: {
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
  .app-divider{
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

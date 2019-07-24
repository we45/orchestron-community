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
              <p class="wordwrap"> <span class="app-created-on">Application</span>  <span class="app-divider">:</span> <strong class="app-value">{{ name }}</strong></p>
               <p class="wordwrap"> <span class="app-created-on">URL</span>  <span class="app-divider">:</span> <span class="app-value">{{ url }}</span></p>
            </b-col>
            <b-col cols="6">
               <p class="wordwrap" v-if="osInfo"> <span class="app-created-on">OS Info </span>  <span class="app-divider">:</span> <span class="app-value">{{ osInfo }}</span></p>
               <p class="wordwrap"> <span class="app-created-on">App Platform</span>  <span class="app-divider">:</span> <span class="app-value">{{ platform }}</span></p>
            </b-col>
          </b-row>

          <!-- <b-btn @click="configureApplication" class="btn-orange">Configure</b-btn> -->
        </b-col>
      </b-row>
      <hr>
      <b-row>
        <b-col cols="10">
            <b-btn @click="configureApplication" class="btn-orange" id="app_config" v-if="enable_Jira">configure</b-btn>
        </b-col>
        <b-col cols="2">
          <b-btn @click="configureWebhook" class="btn-orange">webhook</b-btn>
        </b-col>
      </b-row>

      <br>

    </b-container>
  </div>
</template>

<script>
    import axios from '@/utils/auth'
    export default {
      name: 'AppHeaders',
      props: {
        name: {
          type: String,
          required: true
        },
        logo: {
          required: true
        },
        url: {
          required: true
        },
        osInfo: {
          required: true
        },
        platform: {
          required: true
        },
        enable_Jira: {
          required: false
        }

      },
      data() {
        return {
          appLogo: ''
        }
      },
      mounted() {
        this.fetchData()
      },
      methods: {
        configureWebhook() {
          this.$emit('configureWebhooks', {webhook: true})
        },
        fetchData() {
          if (this.logo) {
            axios.get(this.logo)
              .then(res => {
                this.appLogo = res.data
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 404) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })
          }
        },
        configureApplication() {
          const showConfigure = true
          this.$emit('configureApplication', showConfigure)
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

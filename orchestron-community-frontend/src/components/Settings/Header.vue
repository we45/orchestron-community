<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <b-row v-for="settings in settingsHeader" :key="settings.name">
                <b-col cols="2">
                    <img :src=" 'data:image/png;base64,' + logoOrg" style="height: 120px; width: 120px;" >
                </b-col>
                <b-col cols="10">
                    <b-row>
                        <b-col cols="6">
                            <p class="wordwrap">
                                <span class="app-created-on">Name</span>
                                <span class="app-divider">:</span>
                                <strong class="app-value">{{ settings.name }}</strong>
                            </p>
                            <p class="wordwrap">
                                <span class="app-created-on">Timezone</span>
                                <span class="app-divider">:</span>
                                <span class="app-value">{{ settings.timezone }}</span>
                            </p>
                        </b-col>
                        <b-col cols="6">
                            <p class="wordwrap">
                                <span class="app-created-on">Location </span>
                                <span class="app-divider">:</span>
                                <span class="app-value">{{ settings.location }}</span>
                            </p>
                            <!-- <p class="wordwrap">
                                <span class="app-created-on">Subscription Date</span>
                                <span class="app-divider">:</span> <span class="app-value">{{ settings.endDate }}</span>
                            </p> -->
                        </b-col>
                        <b-btn @click="configureSettings" class="btn-orange">Configure</b-btn>
                         <b-btn @click="updateOrg" class="btn-orange pull-right" id="org_update" style="margin-left: 2%;">Update</b-btn>
                    </b-row>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import axios from '@/utils/auth'

    export default {
      name: 'settingsOrgHeader',
      props: {
        settingsHeader: {
          type: Array,
          required: true
        },
        logoOrg: {
          required: true
        }
      },
      data() {
        return {
          orgLogo: ''
        }
      },
      created() {
        this.fetchData()
      },
      methods: {
        fetchData() {
          let logoPath = ''
          for (const logo of this.settingsHeader) {
            logoPath = logo.logo
          }
          axios.get(logoPath)
            .then(res => {
              this.orgLogo = res.data
            }).catch(error => {
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              } else if (error.res.status === 403) {
                this.$router.push('/forbidden')
              } else {
                this.$router.push('/error')
              }
            })
        },
        configureSettings() {
          const showConfig = true
          this.$emit('configureSettings', showConfig)
        },
        updateOrg() {
          const showConfig = true
          this.$emit('updateOrg', showConfig)
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

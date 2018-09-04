<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
          <loading :active.sync="isLoading" :can-cancel="true"></loading>
            <b-container>
                <br>
                <b-tabs>
                    <b-tab title="profile">
                        <br>
                        <b-row>
                            <b-col sm="4"><label  class="label">First Name:</label></b-col>
                            <b-col sm="8">
                                <b-form-input
                                    v-model="firstName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter First Name" :state="!$v.firstName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row>
                            <b-col sm="4"><label  class="label">Last Name:</label></b-col>
                            <b-col sm="8">
                                <b-form-input
                                    v-model="lastName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Last Name" :state="!$v.lastName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row>
                            <b-col sm="4"><label  class="label">Email:</label></b-col>
                            <b-col sm="8">
                                <b-form-input
                                    v-model="email"
                                    type="email"
                                    class="inline-form-control"
                                    placeholder="Enter Email" :state="!$v.email.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row>
                            <b-col sm="4"><label  class="label">Logo:</label></b-col>
                            <b-col sm="8">
                                <b-form-file
                                    v-model="logo"
                                    placeholder="Choose a logo..."
                                    accept="image/jpeg, image/png,image/jpg,"
                                    :state="!$v.logo.$invalid"></b-form-file>
                            </b-col>
                        </b-row>
                        <br>
                        <br>
                        <b-col col="12">
                            <div class="pull-right" style="float: right">
                                <button type="button" class="btn btn-orange pull-right" data-dismiss="modal" @click=" submitUpdateUser() "
                                    v-if="!$v.firstName.$invalid && !$v.lastName.$invalid && !$v.email.$invalid && !$v.logo.$invalid">
                                Submit
                                </button>
                            </div>
                            <br>
                            <br>
                            <br>
                        </b-col>
                    </b-tab>
                    <b-tab title="Change Password">
                        <br>
                        <form @submit.prevent="submitChangePassword">
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Old Password:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="oldPassword"
                                        type="password"
                                        class="inline-form-control"
                                        placeholder="Old Password" :state="!$v.oldPassword.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">New Password:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="newPassword"
                                        type="password"
                                        class="inline-form-control"
                                        placeholder="New Password" :state="!$v.newPassword.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-row class="my-1">
                                <b-col sm="2"><label class="label">Confirm Password:</label></b-col>
                                <b-col sm="10">
                                    <b-form-input
                                        v-model="confirmPassword"
                                        type="password"
                                        class="inline-form-control"
                                        placeholder="Confirm Password" :state="!$v.confirmPassword.$invalid"></b-form-input>
                                </b-col>
                            </b-row>
                            <br>
                            <b-col col="12" slot="modal-footer">
                                <div class="pull-right" style="float: right;">
                                    <button type="button" class="btn btn-orange"
                                        data-dismiss="modal" @click=" submitChangePassword() " v-if="!$v.oldPassword.$invalid && !$v.newPassword.$invalid && !$v.confirmPassword.$invalid">
                                    Submit
                                    </button>
                                </div>
                            </b-col>
                        </form>
                    </b-tab>
                </b-tabs>
            </b-container>
        </b-container>
    </div>
</template>

<script>
    import axios from '@/utils/auth'
    import { required, minLength, email, sameAs } from 'vuelidate/lib/validators'
    import Loading from 'vue-loading-overlay'
    import 'vue-loading-overlay/dist/vue-loading.min.css'
    import { notValidUser } from '@/utils/checkAuthUser'

    export default {
      name: 'UserProfile',
      components: {
        Loading
      },
      data() {
        return {
          isLoading: false,
          firstName: '',
          lastName: '',
          email: '',
          logo: '',
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      },
      validations: {
        firstName: {
          required,
          minLength: minLength(1)
        },
        lastName: {
          required,
          minLength: minLength(1)
        },
        email: {
          required,
          email,
          minLength: minLength(1)
        },
        logo: {
          // minLength: minLength(0)
        },
        oldPassword: {
          required
          // minLength: 8
        },
        newPassword: {
          required,
          minLength: minLength(8)
        },
        confirmPassword: {
          sameAsPassword: sameAs('newPassword')
        }
      },
      created() {
        this.org = localStorage.getItem('org')
        this.token = localStorage.getItem('token')
        this.fetchData()
      },
      methods: {
        fetchData() {
          if (this.org && this.token) {
            axios.get('/user/profile/')
              .then(res => {
                this.firstName = res.data.first_name
                this.lastName = res.data.last_name
                this.email = res.data.email
                this.logo = res.data.img
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 403) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })
          } else {
            notValidUser()
            this.$router.push('/')
          }
        },
        submitUpdateUser() {
          if (this.org && this.token) {
            const form_data = new FormData()
            form_data.append('first_name', this.firstName)
            form_data.append('last_name', this.lastName)
            form_data.append('email', this.email)
            if(this.logo.name){
                form_data.append('img', this.logo)
            }
            axios.post('/user/profile/', form_data, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
              .then(res => {
                  this.isLoading = true
                  this.$router.go('/org/profile/')
                  this.$notify({
                    group: 'foo',
                    type: 'info',
                    title: 'User',
                    text: 'The user profile has been updated Successfully!',
                    position: 'top right'
                  })
                  this.isLoading = false
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 403) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
              })
          } else {
            notValidUser()
            this.$router.push('/')
          }
        },
        submitChangePassword() {
          if (this.org && this.token) {
            const email = btoa(unescape(encodeURIComponent(localStorage.getItem('email'))))
            const form_data = new FormData()
            form_data.append('old_password', this.oldPassword)
            form_data.append('new_password', this.confirmPassword)
            axios.post('/user/profile/' + email + '/', form_data)
              .then(res => {
                  this.isLoading = true
                  this.$router.go('/org/dashboard')
                  this.$notify({
                    group: 'foo',
                    type: 'success',
                    title: 'User',
                    text: 'The password has been changed Successfully!',
                    position: 'top right'
                  })
                  this.isLoading = false
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 403) {
                  this.$router.push('/forbidden')
                } else {
                  this.$router.push('/error')
                }
            })
          } else {
            notValidUser()
            this.$router.push('/')
          }
        }
      }
    }
</script>

<style scoped>
   .label{
    font-family: 'Avenir';
    font-size: 16px;
    line-height: 1.33;
    color: #000000;
  }

  .inline-form-control {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #ddd;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
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
    /*height: 20px;*/

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

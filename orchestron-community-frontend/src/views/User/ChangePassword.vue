<template>
    <div>
      <b-container fluid>
        <b-card>
        <p class="title">Change Password</p>
        <hr>
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
          <b-col cols="12" slot="modal-footer">
              <div class="pull-right" style="float: right;">
                  <button type="button" class="btn btn-orange"
                      data-dismiss="modal" @click=" submitChangePassword() " v-if="!$v.oldPassword.$invalid && !$v.newPassword.$invalid && !$v.confirmPassword.$invalid">
                  Submit
                  </button>
              </div>
          </b-col>
          </form>
      </b-card>
      </b-container>
    </div>
</template>

<script>
    import axios from '@/utils/auth'
    import { required, sameAs, minLength } from 'vuelidate/lib/validators'
    import { notValidUser } from '@/utils/checkAuthUser'

    export default {
      name: 'ChangePassword',
      data() {
        return {
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      },
      validations: {
        oldPassword: {
          required
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
      },
      methods: {
        submitChangePassword() {
          if (this.org && this.token) {
            const email = btoa(unescape(encodeURIComponent(localStorage.getItem('email'))))
            const form_data = new FormData()
            form_data.append('old_password', this.oldPassword)
            form_data.append('new_password', this.confirmPassword)
            axios.post('/user/password/change/' + email + '/', form_data)
              .then(res => {
                this.$router.push('/org/dashboard')
                this.$notify({
                  group: 'foo',
                  type: 'success',
                  title: 'User',
                  text: 'The password has been changed Successfully!',
                  position: 'top right'
                })
              }).catch(error => {
                if (error.res.status === 404) {
                  this.$router.push('/not_found')
                } else if (error.res.status === 404) {
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
  .title {
    font-family: 'Avenir';
    font-size: 14px;
    font-weight: 600;
    line-height: 0.99;
    text-align: left;
    color: #232328;
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
</style>

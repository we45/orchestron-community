<template>
    <div>
      <!--<b-container fluid>-->
        <b-row>
          <b-col cols="2"></b-col>
          <b-col cols="8">
        <b-card style="margin-top: 10%;">
          <img src="/static/img/login-logo.png" style="height: 220px;width: 100%;border-style:none;border: none;">
        <p class="title">Change Password</p>
        <hr>
        <br>
        <center>

          <p v-if="error_pass['pass']"  class="error"> * {{ error_pass['pass_msg']
                  }}</p>
        </center>
          <br>
          <form @submit.prevent="submitChangePassword">
            <b-row class="my-1">
                <b-col sm="3"><label class="label">New Password:</label></b-col>
                <b-col sm="9">
                    <b-form-input
                        v-model="newPassword"
                        type="password"
                        class="inline-form-control"
                        @input="latest_password_settings(newPassword)"
                        placeholder="New Password" :state="!$v.newPassword.$invalid"></b-form-input>
                        <p class="passFormValid" v-if="!password_test_conditions.leng"> Longer than 7 characters</p>
                        <p class="passFormValid" v-if="!password_test_conditions.caps"> Has a capital letter</p>
                        <p class="passFormValid" v-if="!password_test_conditions.small"> Has a lowercase letter</p>
                        <p class="passFormValid" v-if="!password_test_conditions.num"> Has a number</p>
                        <p class="passFormValid" v-if="!password_test_conditions.spe"> Has a special character</p>
                </b-col>
            </b-row>
            <br>
          <b-row class="my-1">
                <b-col sm="3"><label class="label">Confirm Password:</label></b-col>
                <b-col sm="9">
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
                      data-dismiss="modal" @click=" submitChangePassword() " v-if="!$v.newPassword.$invalid && !$v.confirmPassword.$invalid  && this.password_test_conditions.leng && this.password_test_conditions.caps && this.password_test_conditions.small && this.password_test_conditions.num && this.password_test_conditions.spe">
                  Submit
                  </button>
              </div>
          </b-col>
          </form>
      </b-card>
          </b-col>
           <b-col cols="2"></b-col>
        </b-row>
      <!--</b-container>-->
    </div>
</template>

<script>
    import axios from 'axios'
    import conf from '../../../configure.json'
    import { required, sameAs, minLength } from 'vuelidate/lib/validators'
    import { notValidUser } from '@/utils/checkAuthUser'

    export default {
      name: 'SetNewPassword',
      data() {
        return {
          newPassword: '',
          confirmPassword: '',
          msg: '',
          param: '',
          tokenInfo: '',
          tokenInfoExp: '',
          passResVal: '',
          error_pass: { 'pass': false, 'pass_msg': '' },
          password_test_conditions: {
            'caps': false,
            'num': false,
            'small': false,
            'eight': false,
            'len': false,
            'spe': false
          }
        }
      },
      validations: {
        newPassword: {
          required,
          minLength: minLength(8)
        },
        confirmPassword: {
          sameAsPassword: sameAs('newPassword')
        }
      },
      watch: {
        'newPassword': function(value_name) {
          this.error_pass['pass'] = false
        },
        'confirmPassword': function(value_name) {
          this.error_pass['pass'] = false
        }
      },
      created() {
        this.param = this.$route.params.userToken
        // this.tokenInfo = this.$route.params.tokenInfo
        // this.tokenInfoExp = this.$route.params.tokenInfoExp
        // this.passResVal = this.tokenInfo + this.tokenInfoExp
      },
      methods: {
        submitChangePassword() {
          const baseURL = conf.API_URL
          const loginUrl = baseURL + '/api/user/password/reset/' + this.param + '/'
          axios.post(loginUrl, {
            new_password1: this.newPassword,
            new_password2: this.confirmPassword
          }).then(res => {
            this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The password has been set Successfully!',
                position: 'top right'
              })
            this.msg = res.data.message
              this.$router.push('/')
              this.$router.go('/')

          }).catch(error => {

          }).catch(error => {
              this.$router.push('/')

          }).catch(error => {

            if (error.response.data.detail === 'Signature has expired.') {
              notValidUser()
              this.$router.push('/')
            }
            if (error.response.status === 400) {
              if (error.response.data['error']) {
                this.error_pass['pass'] = true
                this.error_pass['pass_msg'] = error.response.data['error']
              }
            }
          })
        },
        latest_password_settings(password) {
          this.password_test_conditions = { 'caps': false, 'num': false, 'small': false, 'leng': false, 'spe': false }
          var re = /[0-9]/
          if (re.test(password)) {
            this.password_test_conditions.num = true
          }
          var re = /[a-z]/
          if (re.test(password)) {
            this.password_test_conditions.small = true
          }
          var re = /[A-Z]/
          if (re.test(password)) {
            this.password_test_conditions.caps = true
          }
          var re = /[-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]/
          if (re.test(password)) {
            this.password_test_conditions.spe = true
          }

          if (password.length > 7) {
            this.password_test_conditions.leng = true
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

  .error {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 400;
    line-height: 0.99;
    text-align: center;
    color: #f44336;
  }
   .passFormValid {
    font-size: 13px;
    color: #EB0029;
    font-family: 'Avenir';
  }
</style>

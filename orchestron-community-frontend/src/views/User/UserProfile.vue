<template>
  <div>
    <b-container fluid>
      <loading :active.sync="isLoading" :can-cancel="true"></loading>
      <loading :active.sync="isDataLoading" :can-cancel="true"></loading>
      <b-container fluid style="background-color: #FFFFFF;">
        <br>
        <b-row>
          <b-col cols="3">
            <center>
              <template v-if="logo">
                <img :src="'data:image/png;base64,' + logo"  rounded="circle" blank width="250" height="220" blank-color="#777" alt="img" class="m-1" />
              </template>
              <template v-else>
                <b-img-lazy src="/static/img/org.png" rounded="circle" blank width="250" height="220" blank-color="#777" style="background: #f6f6f6;padding: 12px;" alt="img" class="m-1" />
                </template>
              <br>
              <row>
                <!-- <br> -->
                  
                  <p>
                    <!-- <b-badge 
                            class="w3-btn"
                             variant="info"
                             v-b-tooltip.hover="'Copy Token'"
                             style="cursor: pointer;"
                             v-clipboard:copy="token"
                             v-clipboard:success="onCopy"
                             v-clipboard:error="onError">Token
                    </b-badge> -->
                    <template v-if="full_name">
                      <b-badge >{{full_name}}</b-badge>
                    </template>
                    <!-- <template v-if="user_type.admin === 'true'">
                       <b-badge>Admin User</b-badge>
                    </template>
                    <template v-else-if="user_type.superuser ==='true' ">
                      <b-badge>Super User</b-badge>
                    </template>
                    <template v-else>
                      <b-badge>Staff User</b-badge>
                    </template> -->
                  </p>
                <!-- <b-btn v-b-modal.modal1 class="btn-orange">Change Password</b-btn> -->
              </row>
            </center>
          </b-col>
          <b-col cols="8">
            <br>
            <b-row>
              <b-col sm="2"><label class="label_visual">First Name:</label></b-col>
              
              <b-col sm="10">
                <b-form-input
                  v-model="firstName"
                  type="text"
                  maxlength="30"
                  class="visual_text_box"
                  placeholder="Enter First Name" :state="!$v.firstName.$invalid"></b-form-input>
                  <p v-if="error_msgs['first_name']" style="text-align:left;" class="error"> * {{
                        error_msgs['first_name_msg'] }}</p>
                 
              </b-col>
            </b-row>
            <!-- <br> -->
            <b-row>
              <b-col sm="2"><label class="label_visual">Last Name:</label></b-col>
             
              <b-col sm="10">
                <b-form-input
                  v-model="lastName"
                  type="text"
                  maxlength="30"
                  class="visual_text_box"
                  placeholder="Enter Last Name" :state="!$v.lastName.$invalid"></b-form-input>
                    <p v-if="error_msgs['last_name']" style="text-align:left;" class="error"> * {{
                        error_msgs['last_name_msg'] }}</p>
                   
              </b-col>
            </b-row>
            <!-- <br> -->
            <b-row>
              <b-col sm="2"><label class="label_visual">Email:</label></b-col>
              <b-col sm="10">
                <b-form-input
                  v-model="email"
                  type="email"
                  class="visual_text_box"
                  placeholder="Enter Email" :state="!$v.email.$invalid"></b-form-input>
                   <p v-if="error_msgs['email']" style="text-align:left;" class="error"> * {{ error_msgs['email_msg']
                        }}</p>

              </b-col>
            </b-row>
            <!-- <br> -->
            <b-row>
              <b-col sm="2"><label class="label_visual">Logo:</label></b-col>
              <b-col sm="10">
                <b-form-file
                  class="visual_text_box"
                  v-model="logo"
                  placeholder="Choose a logo..."
                  accept="image/jpeg, image/png,image/jpg,"></b-form-file>
                  <p v-if="error_msgs['logo']" style="text-align:left;" class="error"> * {{ error_msgs['logo_msg']
                  }}</p>

              </b-col>
            </b-row>
            <br>
            <!-- <br> -->
            <b-col cols="12">
              <div class="pull-right" style="float: right">
                <button type="button" class="btn btn-orange pull-right" data-dismiss="modal"
                        @click=" submitUpdateUser() "
                        v-if="!$v.firstName.$invalid && !$v.lastName.$invalid && !$v.email.$invalid">
                  Submit
                </button>
              </div>
              
            </b-col>
            <b-col cols="8">
                <btn class="btn btn-orange-submit btn-sm" style="color: #FFFFFF;cursor: pointer;" v-b-modal.modal1>
                          Change Password
                </btn>
            </b-col>
            <br>
              <br>
              <br>
          </b-col>
        </b-row>
      </b-container>

      <!--Change password-->
      <b-modal
        ref="chagePasswordRef"
        title="Change Password"
        size="lg"
        id="modal1"
        centered>
        <div>
          <form @submit.prevent="submitChangePassword">
            <b-row class="my-1">
              <b-col sm="2"><label class="label">Current :</label></b-col>
              <b-col sm="10">
                <b-form-input
                  v-model="oldPassword"
                  type="password"
                  class="inline-form-control"
                  placeholder="Enter current Password"
                  :state="!$v.oldPassword.$invalid"
                ></b-form-input>
                <p v-if="error_msgs_pwd['old']" style="text-align:left;" class="error"> * {{ error_msgs_pwd['old_msg']
                  }}</p>
              </b-col>
            </b-row>
            <br>
            <b-row class="my-1">
              <b-col sm="2"><label class="label">New Password:</label></b-col>
              <b-col sm="10">
                <input placeholder="Enter your password" name="password" class="inline-form-control" type="password" @input="latest_password_settings(newPassword)" v-model="newPassword" />
                <!-- <p class="passFormValid" :class="{'passFormValidPassed' : newPassword.length > 8}"> Longer than 8 characters</p>
                <p class="passFormValid" :class="{'passFormValidPassed' :has_uppercase }"> Has a capital letter</p>
                <p class="passFormValid" :class="{'passFormValidPassed' :has_lowercase }"> Has a lowercase letter</p>
                <p class="passFormValid" :class="{'passFormValidPassed' : has_number }"> Has a number</p>
                <p class="passFormValid" :class="{'passFormValidPassed' : has_special }"> Has a special character</p> -->
                 <!-- {"caps":false, "num":false, "small":false, "eight":false, "len":false}, -->
                <p class="passFormValid"  v-if="!password_test_conditions.len"> Longer than 8 characters</p>
                <p class="passFormValid" v-if="!password_test_conditions.caps"> Has a capital letter</p>
                <p class="passFormValid" v-if="!password_test_conditions.small"> Has a lowercase letter</p>
                <p class="passFormValid" v-if="!password_test_conditions.num"> Has a number</p>
                <p class="passFormValid" v-if="!password_test_conditions.spe"> Has a special character</p>
                 <p v-if="error_msgs_pwd['new']" style="text-align:left;" class="error"> * {{ error_msgs_pwd['new_msg']
                  }}</p>

              </b-col>
            </b-row>
            <br>
            <b-row class="my-1">
              <b-col sm="2"><label class="label">Confirm New Password  :</label></b-col>
              <b-col sm="10">
                <b-form-input
                  v-model="confirmPassword"
                  type="password"
                  class="inline-form-control"
                  placeholder="Enter Confirm Password"
                  :state="!$v.confirmPassword.$invalid"
                ></b-form-input>
                 <p v-if="error_msgs_pwd['new']" style="text-align:left;" class="error"> * {{ error_msgs_pwd['new_msg']
                  }}</p>
              </b-col>
            </b-row>

          </form>
        </div>
        <b-col cols="12" slot="modal-footer">
          <div class="pull-right" style="float: right">
            <button type="button" class="btn btn-orange-close pull-right" @click="closeChangePassword() "> Close
            </button>
            <button type="button"
                    class="btn btn-orange-submit pull-right"
                    data-dismiss="modal"
                    @click=" submitChangePassword() "
                    v-if="!$v.confirmPassword.$invalid  && !$v.newPassword.$invalid && !$v.oldPassword.$invalid"
            >
              Submit
            </button>
          </div>
        </b-col>
      </b-modal>
    </b-container>
  </div>
</template>
<script>
  import axios from '@/utils/auth'
  import {required, minLength, email, sameAs, maxLength} from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import {notValidUser} from '@/utils/checkAuthUser'
  import axios_img from 'axios'

  export default {
    name: 'UserProfile',
    components: {
      Loading
    },
    data() {
      return {
        isDataLoading: false,
        timeout: 2000,
        isLoading: false,
        firstName: '',
        lastName: '',
        email: '',
        logo: '',
        oldLogo: '',
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
        logoFetch: '',
        has_number:    false,
        has_lowercase: false,
        has_uppercase: false,
        has_special:   false,
        UpdateFirstNameError: '',
        UpdateLastNameError: '',
        UpdateEmailError: '',
        UpdateImgError: '',
        password_test_conditions: {"caps":false, "num":false, "small":false, "eight":false, "len":false, "spe":false},
        error_msgs: {
          "name": false,
          "logo": false,
          "name_msg": "",
          "logo_msg": "",
          "first_name": false,
          "first_name_msg": "",
          "last_name": false,
          "last_name_msg": "",
          "email": false,
          "email_msg": ""
        },
        user_type: { "admin": false, "superuser":false, "normal": false},
        error_msgs_pwd: {"old": false, "old_msg": "", "new": false, "new_msg": ""},
        full_name : '',
      }
    },
    validations: {
      firstName: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(30)

      },
      lastName: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(30)

      },
      email: {
        required,
        email,
        minLength: minLength(1)
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
      this.userName = localStorage.getItem('username')
      this.user_type["admin"] = localStorage.getItem('admin')
      this.user_type["superuser"] = localStorage.getItem('superuser')
      this.fetchData()
    },
    watch: {
      'firstName': function (value_name) {
        if (value_name.length > 29) {
          this.error_msgs['first_name'] = true
          this.error_msgs['first_name_msg'] = 'Ensure this field has no more than 30 characters.'
        } else {
          this.error_msgs['first_name'] = false
        }
      },
      'lastName': function (value_name) {
        if (value_name.length > 29) {
          this.error_msgs['last_name'] = true
          this.error_msgs['last_name_msg'] = 'Ensure this field has no more than 30 characters.'
        } else {
          this.error_msgs['last_name'] = false
        }
      },
      'email': function (value_name) {
        if (!this.validEmail(value_name)) {

          this.error_msgs['email'] = true
          this.error_msgs['email_msg'] = "Please Provide Valid Email"

        } else {
          this.error_msgs['email'] = false
        }
      },
      'logo': function (value_name) {
        this.error_msgs['logo'] = false
      },
       'newPassword': function (value_name) {
        this.error_msgs_pwd['new'] = false
      },
      'oldPassword': function (value_name) {
        this.error_msgs_pwd['old'] = false
      },
    },
    methods: {
      fetchData() {
        if (this.org && this.token) {
          this.isDataLoading = true
          setTimeout(() => {
          axios.get('/user/profile/')
            .then(res => {
              this.firstName = res.data.first_name
              this.lastName = res.data.last_name
              this.full_name = res.data.first_name
              this.email = res.data.email
              this.oldLogo = res.data.img
              var api_url = process.env.API_URL
              var imgUrl = api_url+this.oldLogo
            axios.get(imgUrl).then(res=>{
                  this.logo = res.data
                })
              }).catch(error => {
              if (error.response.data.detail === 'Signature has expired.') {
              notValidUser()
              this.$router.push('/')
            }
            if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
          })
          var api_url = process.env.API_URL
          var jwtToken = 'JWT ' + localStorage.getItem('token')

          // const instance = axios.create({
          //   baseURL: api_url,
          //   headers: {
          //     'Authorization': jwtToken
          //   }
          // })
          // var headers =  {
          //     'Authorization': jwtToken
          //   }
       
          
            this.isDataLoading = false
        }, this.timeout);
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
      onCopy: function (e) {
        this.$notify({
          group: 'foo',
          type: 'success',
          title: 'success',
          text: 'The token has been copied successfully!',
          position: 'top right'
        })
      },
      onError: function (e) {
        this.$notify({
          group: 'foo',
          type: 'error',
          title: 'error',
          text: 'The token havent copied!',
          position: 'top right'
        })
      },
      submitUpdateUser() {
        if (this.org && this.token) {

          const form_data = new FormData()
           if (this.logo.name) {
            form_data.append('img', this.logo)
          }else{
            // form_data.append('img', this.oldLogo)
           }
          form_data.append('first_name', this.firstName)
          form_data.append('last_name', this.lastName)
          form_data.append('email', this.email)
          axios.post('/user/profile/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.isLoading = true
              if(this.email != localStorage.getItem('email')){
                localStorage.removeItem('username')
                localStorage.removeItem('token')
                localStorage.removeItem('superuser')
                localStorage.removeItem('admin')
                localStorage.removeItem('email')
                localStorage.removeItem('org')
                this.$router.push('/')
              } 
              else{
                this.fetchData()
              }
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'success',
                text: 'The user profile has been updated successfully!',
                position: 'top right'
              })
              this.isLoading = false
            }).catch(error => {
              if (error.response.data.detail === 'Signature has expired.') {
              notValidUser()
              this.$router.push('/')
            }

              if(error.response.status === 400) {
                 if (error.response.data['first_name']) {
                    this.error_msgs['first_name'] = true
                    this.error_msgs['first_name_msg'] = error.response.data['first_name'][0]
                  }
                  if (error.response.data['img']) {
                    this.error_msgs['logo'] = true
                    this.error_msgs['logo_msg'] = error.response.data['img'][0]
                  }
                  if (error.response.data['last_name']) {
                    this.error_msgs['last_name'] = true
                    this.error_msgs['last_name_msg'] = error.response.data['last_name'][0]
                  }
                  if (error.response.data['email']) {
                    this.error_msgs['email'] = true
                    this.error_msgs['email_msg'] = error.response.data['email'][0]
                  }
              }
              else if (error.response.status === 404) {
              this.$router.push('/not_found')
            } else if (error.response.status === 403) {
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
      password_check () {
            this.has_number    = /\d/.test(this.message);
            this.has_lowercase = /[a-z]/.test(this.message);
            this.has_uppercase = /[A-Z]/.test(this.message);
            this.has_special   = /[!@#\$%\^\&*\)\(+=._-]/.test(this.message);
        },

      latest_password_settings(password){
        this.password_test_conditions = {"caps":false, "num":false, "small":false, "eight":false, "len":false, "spe": false}
          var re = /[0-9]/;
          if(re.test(password)) {
            this.password_test_conditions.num  = true
          }
          var re = /[a-z]/;
          if(re.test(password)) {
             this.password_test_conditions.small  = true
          }
          var re = /[A-Z]/;
          if(re.test(password)) {
            this.password_test_conditions.caps  = true

          }
          var re = /[-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]/;
          if(re.test(password)) {
            this.password_test_conditions.spe  = true

          }

          if(password.length > 7 ){
              this.password_test_conditions.len  = true
          }
      },
      updateScore() {
        this.has_number    = /\d/.test(this.newPassword);
        this.has_lowercase = /[a-z]/.test(this.newPassword);
        this.has_uppercase = /[A-Z]/.test(this.newPassword);
        this.has_special   = /[!@#\$%\^\&*\)\(+=._-]/.test(this.newPassword);


      },
      closeChangePassword() {
        this.$refs.chagePasswordRef.hide()
      },
      submitChangePassword() {
        if (this.org && this.token) {
          const email = btoa(unescape(encodeURIComponent(localStorage.getItem('email'))))
          const form_data = new FormData()
          form_data.append('old_password', this.oldPassword)
          form_data.append('new_password', this.confirmPassword)
          axios.post('/user/password/change/' + email + '/', form_data)
            .then(res => {
              this.isLoading = true
              this.logout()
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'success',
                text: 'The password has been changed successfully!',
                position: 'top right'
              })
              this.isLoading = false
            }).catch(error => {
              if (error.response.data.detail === 'Signature has expired.') {
              notValidUser()
              this.$router.push('/')
            }

              if (error.response.status === 400) {
                if (error.response.data['old_password'] || error.response.data['non_field_errors']) {
                  this.error_msgs_pwd['old'] = true
                  this.error_msgs_pwd['old_msg'] = error.response.data['non_field_errors'][0]
                }
                if (error.response.data['new_password'] || error.response.data['non_field_errors']) {
                  this.error_msgs_pwd['new'] = true
                  this.error_msgs_pwd['new_msg'] = 'Invalid Password'
                }

            }
            if (error.response.status === 404) {
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'error',
                text: 'Invalid Current Password',
                position: 'top right'
              })
              // this.$router.push('/not_found')
            } else if (error.response.status === 403) {
              // this.$router.push('/forbidden')
            } 
            else {
              this.$router.push('/error')
            }
          })
        } else {
          notValidUser()
          this.$router.push('/')
        }
      },
      logout() {
        localStorage.removeItem('username')
        localStorage.removeItem('token')
        localStorage.removeItem('superuser')
        localStorage.removeItem('admin')
        localStorage.removeItem('email')
        localStorage.removeItem('org')
        this.$router.push('/')
      }
    }
  }
</script>
<style scoped>
  .label {
    font-family: 'Avenir';
    font-size: 14px;
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
  .visual_text_box{
    margin: 7px;
    background-color: #f6f6f6;
    border: none;
  }
  .label_visual{
    margin: 7px;
    /*background-color: #f6f6f6;*/
    border: none;
  }

.upload-btn-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
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

  .btn-orange-close {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-close:focus,
  .btn-orange-close.focus {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-close:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;

  }

  .btn-orange-submit:focus,
  .btn-orange-submit.focus {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange-submit:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }
  .passFormValid{
    font-size: 13px;
    color:#EB0029;
    font-family: 'Avenir';
  }
  .passFormValidPassed{
    color:#0fa140;
    font-family: 'Avenir';
  }

  .error{
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 400;
    line-height: 0.99;
    text-align: center;
    color: #f44336;
  }
</style>

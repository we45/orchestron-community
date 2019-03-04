<template>
    <div>
        <b-container fluid>
            <loading :active.sync="isLoading" :can-cancel="true"></loading>
            <common-table :pageCount="projectCount" :dataItems="projectsList"  :headerTitle="headerTitles"
            @createModal="createProject"
            @updateModal="updateProject($event)"
            @deleteModal="beforeDeleteModal($event)"
            @clickPagination="clickPaginations($event)"
            ></common-table>

            <b-modal
                ref="createProjectModal"
                title="Create Project"
                size="lg"
                centered>
                <div>
                    <form @submit.prevent="submitCreateProject">
                        <b-row class="my-1">
                            <b-col sm="2"><label  class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="projectName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Enter Project Name" :state="!$v.projectName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row class="my-1">
                            <b-col sm="2"><label for="input-small" class="label">Logo:</label></b-col>
                            <b-col sm="10">
                                <b-form-file
                                    ref="fileinput"
                                    v-model="projectLogo"
                                    placeholder="Choose a logo..."
                                    accept="image/jpeg, image/png,image/jpg,"
                                    :state="!$v.projectLogo.$invalid"></b-form-file>
                                <br>
                                <p>{{ projectLogo.name }}</p>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right">
                        <button type="button" class="btn btn-orange-close pull-right" @click=" closeCreateProject() "> Close</button>
                        <button type="button" class="btn btn-orange-submit pull-right" data-dismiss="modal" @click=" submitCreateProject() " v-if="!$v.projectName.$invalid && !$v.projectLogo.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <b-modal ref="updateProjectModal" title="Update Project" centered size="lg">
                <div>
                    <form @submit.prevent="submitUpdateProject">
                        <input type="hidden" v-model="updateProjectId">
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Name:</label></b-col>
                            <b-col sm="10">
                                <b-form-input
                                    v-model="updateProjectName"
                                    type="text"
                                    class="inline-form-control"
                                    placeholder="Update Project Name" :state="!$v.updateProjectName.$invalid"></b-form-input>
                            </b-col>
                        </b-row>
                        <br>
                        <b-row class="my-1">
                            <b-col sm="2"><label class="label">Logo:</label></b-col>
                            <b-col sm="10">
                                <b-form-file
                                    v-model="updateProjectLogo"
                                    placeholder="Choose a logo..."
                                    accept="image/jpeg, image/png,image/jpg,"></b-form-file>
                                <br>
                                <br>
                                <p>{{ updateLogoName }}</p>
                                <template v-if="logo">
                                  <b-img-lazy :src="'data:image/png;base64,' + logo" rounded="circle" blank width="250" height="200"  alt="img" />
                                </template>
                            </b-col>
                        </b-row>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeUpdateProject() "> Close</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitUpdateProject() " v-if="!$v.updateProjectName.$invalid">
                        Submit
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <!--Delete Modal-->
            <b-modal ref="beforeDeleteProjectModal" title="Delete Project" centered size="lg">
                <div>
                    <form @submit.prevent="beforeSubmitDeleteProject">
                        <p class="delete-header">Are you sure you want to Delete this Project?</p>
                        <br>
                        <p class="delete-sub">* Deleting this project will delete all Applications and Vulnerabilities associated with it</p>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" beforeCloseDeleteProject() ">No</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" beforeSubmitDeleteProject() ">
                        Yes
                        </button>
                    </div>
                </b-col>
            </b-modal>
            <b-modal ref="deleteProjectModal" title="Delete Project" centered size="lg">
                <div>
                    <form @submit.prevent="submitDeleteProject">
                        <p class="delete-header">* Deleting this project will delete all Applications and Vulnerabilities associated with it</p>
                        <br>
                        <h5 class="text-center">type 'DELETE' to delete the project.</h5>
                      <br>
                      <br>
                        <b-form-input
                            v-model="typeDelete"
                            type="text"
                            class="inline-form-control"
                            placeholder="Type DELETE" ></b-form-input>
                        <br>
                    </form>
                </div>
                <b-col cols="12" slot="modal-footer">
                    <div class="pull-right" style="float: right;">
                        <button type="button" class="btn btn-orange-close" @click=" closeDeleteProject() ">Cancel</button>
                        <button type="button" class="btn btn-orange-submit"
                            data-dismiss="modal" @click=" submitDeleteProject() " v-if="typeDelete==='DELETE'">
                        Delete
                        </button>
                    </div>
                </b-col>
            </b-modal>

        </b-container>
    </div>
</template>

<script>
  import CommonTable from '../../components/Projects/CommonTable'
  import axios from '@/utils/auth'
  import { required, minLength } from 'vuelidate/lib/validators'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.min.css'
  import { notValidUser } from '@/utils/checkAuthUser'

export default {
    name: 'Projects',
    components: {
      CommonTable,
      Loading
    },
    data() {
      return {
        projectsList: [],
        headerTitles: 'List of Projects',
        projectLogo: '',
        projectName: '',
        updateProjectName: '',
        updateProjectLogo: '',
        updateProjectId: '',
        updateLogoName: '',
        typeDelete: '',
        deleteProjectId: '',
        isLoading: false,
        projectCount: 0,
        logo: '',
        full_Data: [],
        isLoadingPage: false,
      }
    },
    validations: {
      projectName: {
        required,
        minLength: minLength(1)
      },
      projectLogo: {
        
      },
      updateProjectName: {
        required,
        minLength: minLength(3)
      }
    },
    created() {
      this.org = localStorage.getItem('org')
      this.token = localStorage.getItem('token')
      this.fetchData()
    },
    updated() {
      this.$nextTick(function() {
        if (this.isLoading) {
          this.projectsList = []
          this.fetchData()
          this.isLoading = false
        }
        if(this.isLoadingPage){

          this.isLoadingPage = false
        }
      })
    },
    methods: {
      fetchData() {
        if (this.org && this.token) {
          axios.get('/organizations/' + this.org + '/?projects=1')
            .then(res => {
              this.full_Data = []
              this.projectCount = res.data.projects_count
              for (const value of res.data.projects) {
                this.full_Data.push({
                  name: { vul_name: value.fields.name },
                  sev: value.stats.severity_count.severity,
                  id: value.fields.id,
                  url: 'individual_project/' + value.fields.id + '/'
                })
              }
            this.projectsList = this.full_Data.slice(0, 5)
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
      createProject() {
        this.$refs.fileinput.reset();
        this.projectLogo = ''
        this.projectName = ''
        this.$refs.createProjectModal.show()
      },
      closeCreateProject() {
        this.$refs.fileinput.reset();
        this.projectLogo = ''
        this.projectName = ''
        this.$refs.createProjectModal.hide()
      },
      submitCreateProject() {
        if (this.org && this.token) {
          const form_data = new FormData()
          form_data.append('logo', this.projectLogo)
          form_data.append('name', this.projectName)
          form_data.append('org', this.org)
          axios.put('/projects/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.$refs.createProjectModal.hide()
              this.isLoading = true
              this.$router.push('/projects/')
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Project',
                text: 'The project has been created Successfully!',
                position: 'top right'
              })
              this.projectLogo = ''
              this.projectName = ''
            }).catch(error => {
              var status_info = error.response.status
              if(status_info === 400){
                  this.$notify({
                    group: 'foo',
                    type: 'error',
                    title: 'Error In Creation of Project',
                    text: 'Project with this Name exists',
                    position: 'top right'
                })
              }
              if (error.res.status === 404) {
                this.$router.push('/not_found')
              }
               else if (error.res.status === 403) {
                this.$router.push('/forbidden')
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
      updateProject(event) {
        if (event.show && this.org && this.token) {
          this.updateProjectName = ''
          this.updateProjectLogo = ''
          this.updateProjectId = ''
          this.updateLogoName = ''
          this.$refs.updateProjectModal.show()
          axios.get('/projects/' + event.id + '/')
            .then(res => {
              this.updateProjectName = res.data.name
              this.updateProjectId = event.id
              const updatelogoSplit = res.data.logo.split('/')
              const logoSplit = updatelogoSplit.pop()
              this.updateLogoName = logoSplit
               axios.get(res.data.logo).then(res=>{
                          this.logo = res.data
                        })                      
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
      closeUpdateProject() {
        this.updateProjectName = ''
        this.updateProjectLogo = ''
        this.updateProjectId = ''
        this.updateLogoName = ''
        this.$refs.updateProjectModal.hide()
      },
      submitUpdateProject() {
        if (this.org && this.token && this.updateProjectId) {
          const form_data = new FormData()
          if (this.updateProjectLogo) {
            form_data.append('logo', this.updateProjectLogo)
          }
          form_data.append('name', this.updateProjectName)
          form_data.append('org', this.org)
          const projectId = this.updateProjectId
          axios.post('/projects/' + projectId + '/', form_data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(res => {
              this.$refs.updateProjectModal.hide()
              this.isLoading = true
              this.$router.push('/projects/')
              this.$notify({
                group: 'foo',
                type: 'info',
                title: 'Project',
                text: 'The project has been updated Successfully!',
                position: 'top right'
              })
              this.updateProjectName = ''
              this.updateProjectLogo = ''
              this.updateProjectId = ''
              this.updateLogoName = ''
            }).catch(error => {
              var status_info = error.response.status
              if(status_info === 400){
                  this.$notify({
                    group: 'foo',
                    type: 'error',
                    title: 'Error In Update of Project',
                    text: 'Project with this Name exists',
                    position: 'top right'
                })
              }
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
      beforeDeleteModal(event) {
        this.deleteProjectId = ''
        this.$refs.beforeDeleteProjectModal.show()
        this.deleteProjectId = event.id
      },
      beforeCloseDeleteProject() {
        this.deleteProjectId = ''
        this.$refs.beforeDeleteProjectModal.hide()
      },
      closeDeleteProject() {
        this.deleteProjectId = ''
        this.$refs.beforeDeleteProjectModal.hide()
      },
      beforeSubmitDeleteProject() {
        this.$refs.deleteProjectModal.show()
      },
      clickPaginations(event) {
          if (event.page) {
            if (event.page > 1) {
                var page_no = event.page
                this.projectsList = this.full_Data.slice(5*(page_no-1), 5*(page_no))
                this.isLoadingPage = true
            } else {
              this.fetchData()
            }
          }
          else {
            // notValidUser()
            // this.$router.push('/')
          }
        },
      submitDeleteProject() {
        if (this.org && this.token) {
          axios.delete('/projects/' + this.deleteProjectId + '/')
            .then(res => {
              this.$refs.deleteProjectModal.hide()
              this.isLoading = true
              this.$router.push('/projects/')
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'Project',
                text: 'The project has been deleted Successfully!',
                position: 'top right'
              })
              this.deleteProjectId = ''
              // this.deleteProjectId = ''
              this.typeDelete = ''
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

  .label {
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

  .delete-header {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 500;
    line-height: 0.99;
    text-align: center;
    color: #232325;
  }

  .delete-sub {
    font-family: 'Avenir';
    font-size: 16px;
    font-weight: 400;
    line-height: 0.99;
    text-align: center;
    color: #232325;
  }
</style>

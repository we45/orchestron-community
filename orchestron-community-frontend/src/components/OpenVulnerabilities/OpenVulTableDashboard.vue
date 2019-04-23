<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
                <br>

                <b-row v-if="isSearch">
                  <b-col cols="8">
                    <b-row>
                      <!--<b-col sm="10">-->
                      <b-col sm="2">
                        <label for="">Search by: </label>
                      </b-col>
                      <b-col sm="4">
                        <v-select  v-model="filterType" :options="filterOptions"
                                   placeholder="Select search"
                                   @input="selectedFilterType" v-if="isOpenVul"></v-select>
                        <v-select  v-model="filterType" :options="filternoSevOptions"
                                   placeholder="Select search"
                                   @input="selectedFilterType" v-else></v-select>
                      </b-col>
                      <b-col sm="4">
                        <b-form-input
                          v-model="filter"
                          placeholder="Search CWE"
                          class="inline-form-control"
                          v-if="filterType.value==='cwe'"
                          type="number"/>
                        <b-form-input v-model="filter" placeholder="Search Vulnerabilities" class="inline-form-control" v-if="filterType.value==='vul_name'"/>
                        <v-select  v-model="filter" :options="filterSevOptions" placeholder="Select Severities" v-if="filterType.value==='sev'"></v-select>
                      </b-col>
                      <b-col cols="1">
                        <b-button
                          size="sm"
                          v-if="filterType.value && filter"
                          @click="searchFilteredValue($event)"
                          class="btn btn-orange">search</b-button>
                      </b-col>
                      <b-col cols="1" v-if="(filterType.value==='vul_name' || filterType.value==='sev' || filterType.value==='cwe') && filter">
                        <b-button
                          @click="default_state()"
                          class="button_clear">Clear Filter</b-button>
                      </b-col>
                    </b-row>
                    <!-- <b-row>

              </b-row> -->
                  </b-col>
                  <b-col cols="4">
                    <b-pagination :total-rows="numPages"
                            :per-page="perPage"
                            v-model="currentPage" class="my-1" align="right" @input="paginationClick(currentPage)"></b-pagination>
                  </b-col>
                </b-row>
                <b-row v-else>
                  <b-col cols='8'>

                  </b-col>
                  <b-col cols="4">
                    <b-pagination :total-rows="numPages"
                            :per-page="perPage"
                            v-model="currentPage" class="my-1" align="right" @input="paginationClick(currentPage)"></b-pagination>
                  </b-col>
                </b-row>
                <br>
                <b-table show-empty
                    stacked="md"
                    :items="dataItems"
                    :fields="fields"
                    :current-page="currentPage"
                    :per-page="perPage"
                    :sort-by.sync="sortBy"
                    :sort-desc.sync="sortDesc"
                    class="m2_top">
                    <template slot="sev" slot-scope="row">
                        <div class="high-vul-severity-line" v-if="row.item.sev===3"></div>
                        <div class="medium-vul-severity-line" v-if="row.item.sev===2"></div>
                        <div class="low-vul-severity-line" v-if="row.item.sev===1"></div>
                        <div class="info-vul-severity-line" v-if="row.item.sev===0"></div>
                    </template>
                    <template slot="name" slot-scope="row">
                      <b-row >
                        <b-col cols="8">
                          <!-- <template v-if="row.item.tool === 'Manual'">
                                <label>
                                  <b-form-checkbox v-model="bulkData" v-bind:value="row.item.commonName"    class="mb-2 mr-sm-2 mb-sm-0"></b-form-checkbox>
                                </label>
                                <p   style="float: left;" class="title"  v-b-tooltip.hover :title="row.item.commonName">{{row.item.commonName}}</p>
                          </template> -->
                          <template >
                              <label style="float: left;" v-if="(bulkMarking === 'FalsePositive') || (bulkMarking  === 'TruePositive') || (bulkMarking  === 'DeleteVulnerabilities')">
                                <b-form-checkbox  @input="bulkDataValues" v-model="bulkData" v-bind:value="row.item.commonName"  class="mb-2 mr-sm-2 mb-sm-0"></b-form-checkbox>
                              </label>
                              <p  class="title" v-b-tooltip.hover :title="row.item.commonName">{{row.item.commonName}}</p>
                          </template>
                        </b-col>
                        <!-- <b-col cols="4">
                          <b-badge variant="danger" v-if="row.item.cwe===0" pill
                                   style="cursor: pointer" @click="updateUncategorized(row.item.commonName)">Uncategorized</b-badge>
                        </b-col> -->
                      </b-row>

                      <!--<b-row v-else="!row.item.multiple">-->
                        <!--<b-col cols="8">-->
                          <!--<p class="title" v-b-tooltip.hover :title="row.item.commonName">{{row.item.commonName}}</p>-->
                        <!--</b-col>-->
                        <!--<b-col cols="4">-->
                            <!--<b-badge variant="danger" v-if="row.item.cwe===0" pill>Uncategorized</b-badge>-->
                        <!--</b-col>-->
                      <!--</b-row>-->


                        <b-row>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">CWE</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.cwe }}</span>
                                </p>
                            </b-col>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Open For</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value" >{{ row.item.openFor }} days ago</span>
                                </p>
                            </b-col>
                        </b-row>
                    </template>
                    <template slot="actions" slot-scope="row">
                        <p><span class="second-sub-title">Tools : </span> <span class="second-sub-name">{{ row.item.tool }}</span></p>
                        <p v-if=" row.item.apps.length === 1">
                            <span class="second-sub-title">App : </span>
                            <b-button size="sm" @click="viewIndividualVul(row.item.app, row.item.commonName)" class="mr-1 btn-orange"
                                >
                                {{ row.item.app }}
                            </b-button>
                        </p>
                      <p v-else>
                        <span class="second-sub-title">Apps : </span>
                        <span class="dropdown" style="cursor: pointer">
                          <button class="orchy-btn-hover" style="cursor: pointer"  >Apps</button>
                          <label style="cursor: pointer">
                            <input type="checkbox" id="multipleClose"  @click="accordian_close($event)">
                            <ul>
                              <template v-for="(value) in row.item.apps" v-if="row.item.app.length > 1">
                                <li @click="viewIndividualVul(value, row.item.commonName)">{{ value }}</li>
                              </template>
                            </ul>
                          </label>
                        </span>
                      </p>
                    </template>
                </b-table>
        </b-container>
    </div>
</template>

<script>
const items = []

export default {
  name: 'OpenVulTableDashboard',
  data() {
    return {
      counter: 45,
      max: 200,
      items: '',
      fields: [
        { key: 'sev', label: ' ', sortable: true, 'class': 'title' },
        { key: 'name', label: 'Vulnerability Name', sortable: true, 'class': 'title' },
        { key: 'actions', label: ' ', 'class': 'title', sortable: false }
      ],
      currentPage: 0,
      perPage: 5,
      totalRows: 0,
      pageOptions: [5, 10, 15],
      sortBy: null,
      sortDesc: false,
      filter: null,
      numPages: 0,
      filterType: '',
      bulkData : [],
      filterOptions: [
        { label: 'Name', value: 'vul_name' },
        { label: 'CWE', value: 'cwe' },
        { label: 'Severity', value: 'sev' }
      ],
      filternoSevOptions: [
        { label: 'Name', value: 'vul_name' },
        { label: 'CWE', value: 'cwe' }
      ],
      filterSevOptions: [
        { label: 'High', value: 3 },
        { label: 'Medium', value: 2 },
        { label: 'Low', value: 1 },
        { label: 'Info', value: 0 }
      ]
    }
  },
  props: {
    dataItems: {
      type: Array,
      required: true
    },
    pageNumberCount: {
      required: false
    },
    pageCurrent: {
      required: false
    },
    isOpenVul: {
      required: false
    },
    isSearch:{
      required: false
    },
    bulkMarking:{
      required: false
    }
  },
  beforeUpdate() {
    this.items = this.dataItems
    this.numPages = this.pageNumberCount
    this.currentPage = this.pageCurrent
  },
  computed: {
    sortOptions() {
      return this.fields
        .filter(f => f.sortable)
        .map(f => { return { text: f.label, value: f.key } })
    }
  },
  methods: {
    viewIndividualVul(app, name) {
      const encodedApp = btoa(unescape(encodeURIComponent(app)))
      const encodedName = btoa(unescape(encodeURIComponent(name)))
      // const encodedCwe = btoa(unescape(encodeURIComponent(cwe)))
      this.$router.push({ path: '/org/individual_vul/' + encodedApp + '/' + encodedName })
    },

    accordian_close(evt) {
      var buttonClick = document.querySelectorAll('[id^="multipleClose"]')
      for (var i = 0; i < buttonClick.length; i++) {
        if (parseInt(Array.from(buttonClick).indexOf(evt.target)) !== i) {
          if (buttonClick[i].checked) {
            buttonClick[i].click()
          }
        }
      }
    },
    paginationClick(currentPage) {
      this.$emit('clickPagination', { page: currentPage })
    },
    updateUncategorized(commonName) {
      this.$emit('updateUncategorized', { commonName: commonName })
    },
    default_state(){
      this.filterType = ''
      this.$emit('resetFilter')
    },
    selectedFilterType(){
      this.filter = ''
    },
    bulkDataValues() {
      this.$emit('bulkDataValues', {values: this.bulkData})
    },
    searchFilteredValue(event) {
       if (this.filterType.value === 'sev') {
        this.$emit('searchFilteredValue', { searchType: this.filterType.value, searchValue: this.filter.value})
         this.filter = this.filter.label
      }else{
         this.$emit('searchFilteredValue', { searchType: this.filterType.value, searchValue: this.filter})
       }
    }

  }
}
</script>

<style scoped>
  .dropdown {
  position: relative;
  display: inline-block;
  font-family: 'Avenir';
  font-size: 14px;
    cursor: pointer;
}
  .orchy-btn-hover:hover {
  position: relative;
  display: inline-block;
    color: #FFFFFF;
  background-color: #ff542c;
  font-family: 'Avenir';
  font-size: 14px;
    cursor: pointer;
}

.dropdown > .orchy-btn-hover {
  color: #ff542c;
  background-color: #FFFFFF;
  font-family: 'Avenir';
  border-radius: 14px;
  font-size: 14px;
  border: 1px solid #ff542c;
  padding: 6px 20px 6px 10px;
  display: inline-block;
  text-decoration: none;
  cursor: pointer;
}
 .dropdown > .orchy-btn-hover:focus {
  color: #ff542c;
  background-color: #FFFFFF;
  font-family: 'Avenir';
  border-radius: 14px;
  font-size: 14px;
  border: 1px solid #ff542c;
  padding: 6px 20px 6px 10px;
  display: inline-block;
  text-decoration: none;
    cursor: pointer;
}
 .dropdown > .orchy-btn-hover:hover {
  color: #ff542c;
  background-color: #ff542c;
  font-family: 'Avenir';
  border-radius: 14px;
  font-size: 14px;
  border: 1px solid #FFFFFF;
  padding: 6px 20px 6px 10px;
  display: inline-block;
  text-decoration: none;
    cursor: pointer;
}

.dropdown > .orchy-btn-hover:before {
  position: absolute;
  right: 7px;
  top: 12px;
  content: ' ';
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #F04E23;
}

.dropdown input[type=checkbox] {
  position: absolute;
  display: block;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  margin: 0px;
  opacity: 0;
  color: #F04E23;
  background-color: #F04E23;
}

.dropdown input[type=checkbox]:checked {
  position: fixed;
  z-index:+0;
  top: 0px; left: 0px;
  right: 0px; bottom: 0px;
  color: #F04E23;
  background-color: #F04E23;
}

.dropdown ul {
  position: absolute;
  top: 18px;
  border: 1px solid #ccc;
  border-radius: 3px;
  left: 60px;
  list-style: none;
  padding: 4px 0px;
  display: none;
  background-color: white;
  box-shadow: 0 3px 6px #F04E23;
}

.dropdown input[type=checkbox]:checked + ul {
  display: block;

}

.dropdown ul li {
  display: block;
  padding: 6px 20px;
  white-space: nowrap;
  min-width: 100px;
}

.dropdown ul li:hover {
  background-color: #F5F5F5;
  cursor: pointer;

}

.dropdown ul li a {
  text-decoration: none;
  display: block;
  color: #F04E23;
}

.dropdown .divider {
  height: 1px;
  margin: 9px 0;
  overflow: hidden;
  background-color: #e5e5e5;
  font-size: 1px;
  padding: 0;
}


  .title {
    font-family: 'Avenir';
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    width: 500px;
    text-overflow: ellipsis;
    text-align: left;
  }

  .high-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #d11d55;
    margin-top: 15%;
  }

  .medium-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #ff9c2c;
    margin-top: 15%;
  }

  .low-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #008b8f;
    margin-top: 15%;
  }

  .info-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #1d1e52;
    margin-top: 15%;
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

  .sub-title {
    width: 200px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: left;
    color: #6b7784;
  }

  .sub-divider {
    width: 10px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }

  .sub-value {
    width: 100px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }

  .second-sub-title {
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.5;
    color: #979797;
  }

  .second-sub-name {
    font-family: 'Avenir';
    font-size: 12px;
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
  .button_clear{
    background: none;
    color: rgb(80, 95, 121);
    cursor: pointer;
    border: none;
    font: 14px 'Avenir';
  }
  .button_clear:hover{
    background: rgba(9, 30, 66, 0.04);
    font: 14px 'Avenir';
  }

  orchy {
display: inline-block;
padding: 9px 12px;
padding-top: 7px;
margin-bottom: 0;
font-size: 14px;
line-height: 20px;
color: #5e5e5e;
text-align: center;
vertical-align: middle;
cursor: pointer;
background-color: #d1dade;
-webkit-border-radius: 3px;
-webkit-border-radius: 3px;
-webkit-border-radius: 3px;
background-image: none !important;
border: 1px #F04E23;
text-shadow: none;
box-shadow: none;
transition: all 0.12s linear 0s !important;
font: 14px/20px "Helvetica Neue",Helvetica,Arial,sans-serif;
}

</style>

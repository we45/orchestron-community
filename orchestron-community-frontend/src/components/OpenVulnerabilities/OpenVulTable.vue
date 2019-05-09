<template>
  <div>
    <b-container fluid style="background-color: #FFFFFF;">
      <b-col cols="12">
        <br>
        <b-row>
          <b-col md="6" class="my-1">
            <b-form-input v-model="filter" placeholder="Type to Search" class="inline-form-control"/>
          </b-col>
          <b-col md="2"></b-col>
          <b-col md="4" class="my-1">
          </b-col>
        </b-row>
        <b-row>
          <b-col md="6" class="my-1">
          </b-col>
          <b-col md="6" class="my-1">
            <b-pagination :total-rows="numPages"
                          :per-page="perPage"
                          v-model="currentPage" class="my-1" align="right"
                          @input="paginationClick(currentPage)"></b-pagination>
          </b-col>
        </b-row>
        <b-table show-empty
                 stacked="md"
                 :items="dataItems"
                 :fields="fields"
                 :current-page="currentPage"
                 :per-page="perPage"
                 :filter="filter"
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
            <p v-if="row.item.multiple" class="title" v-b-tooltip.hover :title="row.item.commonName">
              {{row.item.commonName}} - Multiple</p>
            <p v-else="!row.item.multiple" class="title" v-b-tooltip.hover :title="row.item.commonName">
              {{row.item.commonName}}</p>
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
                  <span class="sub-value">{{ row.item.openFor }} days ago</span>
                </p>
              </b-col>
               <b-col cols="2" v-if="isUncategorised && !row.item.multiple">
                              <b-badge variant="danger" v-if="row.item.cwe===0" pill
                                       style="cursor: pointer" @click="updateUncategorized(row.item.commonName)">Uncategorized
                              </b-badge>
                            </b-col>
            </b-row>
          </template>
          <template slot="actions" slot-scope="row">
            <p><span class="second-sub-title">Tools : </span> <span class="second-sub-name">{{ row.item.tool }}</span>
            </p>
            <p>
              <span class="second-sub-title" v-if="!row.item.multiple">Apps : </span>
              <b-button size="sm" @click="viewIndividualVul(row.item.app, row.item.vulName, row.item.cwe)"
                        class="mr-1 btn-orange"
                        v-if="!row.item.multiple">
                {{ row.item.app }}
              </b-button>
            </p>
            <b-button size="sm" @click.stop="row.toggleDetails" @click="accordian_close($event)" id="multipleClose"
                      class="btn-orange" v-if="row.item.multiple">
              {{ row.detailsShowing ? 'Hide' : 'Show' }}-Details
            </b-button>
          </template>
          <template slot="row-details" slot-scope="row" v-if="row.item.multiple">
            <b-card>
              <b-row v-model="cwe_val_multiple = row.item.cwe">
                <b-col cols="12">
                  <b-pagination size="md" align="right" :total-rows="Object.keys(row.item.name).length"
                                v-model="currentPage_multiple" :per-page="5">
                  </b-pagination>
                </b-col>
              </b-row>
              <b-table
                show-empty
                stacked="sm"
                :current-page="currentPage_multiple"
                :fields="multipleFields"
                :items="Object.entries(row.item.name)"
                :per-page="5"
                :filter="filter_inside"
                :sort-by.sync="sortBy"
                class="m2_top"
              >
                <template slot="name_multiple" slot-scope="row" v-for="(value, key) in row.item.name">
                  <b-row>
                    <b-col>
                      <b-list-group>
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                          <b-row>
                            <b-col cols="10">
                              {{ row.item[0] }}
                            </b-col>
                            <b-col cols="2" v-if="isUncategorised">
                              <b-badge variant="danger" v-if="cwe_val_multiple===0" pill
                                       style="cursor: pointer" @click="updateUncategorized(row.item)">Uncategorized
                              </b-badge>
                            </b-col>
                          </b-row>

                          <b-button size="sm" @click="viewIndividualVul(row.item[1], row.item[0], cwe_val_multiple)"
                                    class="mr-1 btn-orange">
                            {{ row.item[1] }} 
                          </b-button>

                        </b-list-group-item>
                        <br>
                      </b-list-group>
                    </b-col>
                  </b-row>
                </template>
              </b-table>
              <!--  <template  v-for="(value, key) in row.item.name">
                   <b-row>
                       <b-col>
                           <b-list-group>
                               <b-list-group-item class="d-flex justify-content-between align-items-center">
                                   {{ key }}
                                   <b-button size="sm" @click="viewIndividualVul(value, key, row.item.cwe)" class="mr-1 btn-orange">
                                       {{ value }}
                                   </b-button>
                               </b-list-group-item>
                               <br>
                           </b-list-group>
                       </b-col>
                   </b-row>
               </template> -->
            </b-card>
          </template>
        </b-table>
      </b-col>
    </b-container>
  </div>
</template>

<script>
  // const items = []
  const items = []
  export default {
    name: 'OpenVulTable',
    data() {
      return {
        counter: 45,
        max: 200,
        items: '',
        fields: [
          {key: 'sev', label: ' ', sortable: true, 'class': 'title'},
          {key: 'name', label: 'Vulnerability Name', sortable: true, 'class': 'title'},
          {key: 'actions', label: ' ', 'class': 'title', sortable: false}
        ],
        multipleFields: [
          {key: 'name_multiple', label: 'Multiple Vulnerabilities', sortable: false, 'class': 'title'},
        ],
        currentPage: 0,
        currentPage_multiple: 1,
        perPage: 5,
        totalRows: 0,
        pageOptions: [5, 10, 15],
        pageOptions_multiple: [5, 10, 15, 20, 25],
        sortBy: null,
        filter_inside: null,
        sortDesc: false,
        filter: null,
        numPages: 0,
        selected: {},
        multiple_perPage: 5,
        cwe_val_multiple: 0
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
      isUncategorised: {
        required: false,
        default: true
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
          .map(f => {
            return {text: f.label, value: f.key}
          })
      }
    },
    methods: {
      updateUncategorized(commonName) {
        this.$emit('updateUncategorized', {commonName: commonName})
      },
      viewIndividualVul(app, name, cwe) {
        const encodedApp = btoa(unescape(encodeURIComponent(app)))
        const encodedName = btoa(unescape(encodeURIComponent(name)))
        const encodedCwe = btoa(unescape(encodeURIComponent(cwe)))
        this.$router.push({path: '/org/individual_vul/' + encodedApp + '/' + encodedName + '/' + encodedCwe})
      },
      paginationClick(currentPage) {
        this.$emit('clickPagination', {page: currentPage})
      },
      accordian_close(evt) {
        var buttonClick = document.querySelectorAll('[id^="multipleClose"]');
        var xy = Array.from(buttonClick).indexOf(evt.target)
        for (var i = 0; i < buttonClick.length; i++) {
          if (xy != i) {
            var split_txt = buttonClick[i].innerText.split('-')[0]
            if (split_txt == 'Hide') {
              buttonClick[i].click()
            }
          }
        }
      }
    }
  }
</script>

<style scoped>
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
</style>

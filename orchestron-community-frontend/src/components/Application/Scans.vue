<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <b-col cols="12">
                <br>
                <b-row>
                    <b-col md="6" class="my-1">
                        <b-form-input
                          v-model="filter"
                          placeholder="Type to Search"
                          class="inline-form-control"/>
                    </b-col>
                    <b-col md="2"></b-col>
                    <b-col md="4" class="my-1">
                        <b-form-select
                          :options="pageOptions"
                          v-model="perPage"/>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col md="6" class="my-1">
                    </b-col>
                    <b-col md="6" class="my-1">
                        <b-pagination
                          :total-rows="totalRows"
                          :per-page="perPage"
                          v-model="currentPage"
                          class="my-1"
                          align="right"/>
                    </b-col>
                </b-row>
                <!-- Main table element -->
                <b-table show-empty
                    stacked="md"
                    :items="dataItems"
                    :fields="fields"
                    :current-page="currentPage"
                    :per-page="perPage"
                    :filter="filter"
                    :sort-by.sync="sortBy"
                    :sort-desc.sync="sortDesc"
                    @filtered="onFiltered"
                    class="m2_top">
                    <template slot="sev" slot-scope="row" v-if="row.item.appDashboard">
                        <!--<b-form-checkbox-->
                          <!--@click.native.stop-->
                          <!--@change="row.toggleDetails"-->
                          <!--v-model="row.detailsShowing" >-->
                        <!--</b-form-checkbox>-->
                    </template>
                    <template slot="name" slot-scope="row">
                        <p class="title">
                          <router-link :to="row.item.url">
                            {{ row.item.name}}
                          </router-link>
                        </p>
                      <template>
                          <vul-progress-bar
                          :high="row.item.sev[3] || 0"
                          :medium="row.item.sev[2] || 0"
                          :low="row.item.sev[1] || 0"
                          :info="row.item.sev[0] || 0"
                          :total="row.item.sev | checkSev"></vul-progress-bar>
                        </template>
                        <b-row>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Date</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.scanDate | moment("MMMM Do YYYY") }}</span>
                                </p>
                              <p>
                                    <span class="sub-title">Scan Triggered By</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.triggeredBy }}</span>
                                </p>
                            </b-col>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Scan Type</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value" >{{ row.item.scanType }}</span>
                                </p>
                              <p>
                                    <span class="sub-title">Tool</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value" >{{ row.item.tool }}</span>
                                </p>
                            </b-col>
                        </b-row>
                    </template>
                    <template slot="actions" slot-scope="row" v-if="row.item.appDashboard">
                      <b-button
                        size="sm"
                        @click="deleteModal(row.item.scanId)"
                        class="mr-1 btn-orange">
                          Delete
                        </b-button>
                    </template>
                </b-table>
            </b-col>
        </b-container>
    </div>
</template>
<script>
  import VulProgressBar from '@/components/OpenVulnerabilities/VulProgressBar'
  const items = []
  export default {
    name: 'Scans',
    props: {
      dataItems: {
        type: Array,
        required: false
      }
    },
    components: {
      VulProgressBar
    },
    data() {
      return {
        items: '',
        fields: [
          { key: 'sev', label: ' ', sortable: true, 'class': 'title' },
          { key: 'name', label: 'Scan Name', sortable: true, 'class': 'title' },
          { key: 'actions', label: ' ', 'class': 'title', sortable: false }
        ],
        currentPage: 1,
        perPage: 5,
        totalRows: items.length,
        pageOptions: [5, 10, 15],
        sortBy: null,
        sortDesc: false,
        filter: null,
        showModal: true
      }
    },
    beforeUpdate() {
      this.items = this.dataItems
    },
    methods: {
      deleteModal(id) {
        this.$emit('deleteModal', { id: id, show: this.showModal })
      },
      onFiltered(filteredItems) {
        this.totalRows = filteredItems.length
        this.currentPage = 1
      }
    }
  }
</script>

<style scoped>
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

  .sub-title {
    width: 200px;
    height: 8px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: left;
    color: #6b7784;
  }

  .sub-divider {
    width: 10px;
    height: 8px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }

  .sub-value {
    width: 100px;
    height: 8px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }
</style>

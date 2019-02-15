<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <br>
            <p class="title"> {{ headerTitle }} </p>
          <hr>
            <b-col cols="12">

              <b-btn @click="createModal" class="btn-orange" v-if="!createButton">Create</b-btn>
              <br>
              <br>
                <b-row>
                    <b-col md="6" class="my-1">
                        <b-form-input v-model="filter" placeholder="Type to Search" class="inline-form-control"/>
                    </b-col>
                    <b-col md="1"></b-col>
                    <b-col md="5">
                      <b-pagination :total-rows="numPages"
                                    :per-page="perPage"
                                    v-model="currentPage"
                                    align="right"
                                    @input="paginationClick(currentPage)"></b-pagination>
                    </b-col>
                </b-row>
                <br>
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
                    <template slot="name" slot-scope="row">
                    <router-link :to="row.item.url">
                          <p class="title">
                            {{ row.item.name.vul_name }}
                          </p>
                    </router-link>
                      <b-row v-if="row.item.appName || row.item.engId">
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Application</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.appName }}</span>
                                </p>
                            </b-col>
                            <b-col cols="8">
                                <p>
                                    <span class="sub-title">Engagement ID</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value" >{{ row.item.engId }}</span>
                                </p>
                            </b-col>
                        </b-row>
                      <vul-progress-bar
                  :high="row.item.sev[3]"
                  :medium="row.item.sev[2]"
                  :low="row.item.sev[1]"
                  :info="row.item.sev[0]"
                  :total="row.item.sev | checkSev" v-if="Object.keys(row.item.sev).length !== 0"></vul-progress-bar>
                    </template>
                    <template slot="actions" slot-scope="row">
                        <b-button size="sm" class="btn-orange" style="float: right;" @click="deleteModal(row.item.id)" v-if="!deleteButton">
                Delete
              </b-button>
              <b-button size="sm" class="btn-orange" style="float: right; margin-right: 3%;" @click="updateModal(row.item.id)">
                Update
              </b-button>
                    </template>
                </b-table>
            </b-col>
        </b-container>
    </div>
</template>

<script>
const items = []
import VulProgressBar from '@/components/OpenVulnerabilities/VulProgressBar'
export default {
  name: 'CommonTable',
  components: {
    VulProgressBar
  },
  data() {
    return {
      counter: 45,
      max: 200,
      items: '',
      fields: [
        { key: 'name', label: 'Name', sortable: true, 'class': 'title' },
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
      showModal: true
    }
  },
  props: {
    dataItems: {
      type: Array,
      required: true
    },
    headerTitle: {
      type: String,
      required: true
    },
    pageCount: {
      required: false
    },
    createButton: {
      type: Boolean,
      required: false
    },
    deleteButton: {
      type: Boolean,
      required: false
    }
  },
  beforeUpdate() {
    this.items = this.dataItems
    this.numPages = this.pageCount
  },
  computed: {
    sortOptions() {
      return this.fields
        .filter(f => f.sortable)
        .map(f => { return { text: f.label, value: f.key } })
    }
  },
  methods: {
    onFiltered() {
      this.totalRows = this.numPages
    },
    createModal() {
      this.$emit('createModal', this.showModal)
    },
    updateModal(id) {
      this.$emit('updateModal', { id: id, show: this.showModal })
    },
    deleteModal(id) {
      this.$emit('deleteModal', { id: id, show: this.showModal })
    },
    // paginationClick(page) {
    //   this.currentPage = page
    //   this.$emit('pagination', { page: this.currentPage })
    // },
    paginationClick(page) {
      this.$emit('clickPagination', { page: page })
    },
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
</style>

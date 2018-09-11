<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <b-col cols="12">
                <br>
                <p class="title"> {{ headerTitle }} </p>
                <hr>
                <br>
                <b-button size="sm" @click="createModal()" class="mr-1 btn-orange" style="float: left;">
                    Create
                </b-button>
                <br>
                <br>
                <b-row>
                    <b-col md="6" class="my-1">
                        <b-form-input v-model="filter" placeholder="Type to Search" class="inline-form-control"/>
                    </b-col>
                    <b-col md="2"></b-col>
                    <b-col md="4" class="my-1">
                        <b-form-select :options="pageOptions" v-model="perPage"/>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col md="6" class="my-1">
                    </b-col>
                    <b-col md="6" class="my-1">
                        <b-pagination :total-rows="numPages"
                                      :per-page="perPage" 
                                      v-model="currentPage" 
                                      class="my-1" @input="paginationClick(currentPage)" align="right"/>
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
                    @filtered="onFiltered"
                    class="m2_top">
                    <template slot="name" slot-scope="row">
                        <p class="title">{{ row.item.name }}</p>
                        <b-row>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Application</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.app }}</span>
                                </p>
                            </b-col>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">Tool</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value" >{{ row.item.tool }} </span>
                                </p>
                            </b-col>
                        </b-row>
                    </template>
                    <template slot="actions" slot-scope="row">
                        <b-button size="sm" @click="deleteModal(row.item.id)" class="mr-1 btn-orange" style="float: right;">
                            Delete
                        </b-button>
                        <b-button size="sm" @click="updateModal(row.item.id)" class="mr-1 btn-orange" style="float: right;">
                            Update
                        </b-button>
                        <b-button size="sm" @click="copyModal(row.item.id)" class="mr-1 btn-orange" style="float: right;">
                            Copy
                        </b-button>
                    </template>
                </b-table>
            </b-col>
        </b-container>
    </div>
</template>

<script>
const items = []

export default {
  name: 'WebHookCommonTable',
  data() {
    return {
      counter: 45,
      max: 200,
      items: '',
      fields: [
        { key: 'name', label: 'Name', sortable: true, 'class': 'title' },
        { key: 'actions', label: ' ', 'class': 'title', sortable: false }
      ],
      currentPage: 1,
      perPage: 5,
      totalRows: items.length,
      pageOptions: [5, 10, 15],
      sortBy: null,
      sortDesc: false,
      filter: null,
      showModal: false,
      numPages: 0
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
    }
  },
  beforeUpdate() {
    this.items = this.dataItems
    this.numPages = this.pageCount
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
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
      this.currentPage = 1
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
    copyModal(id) {
      this.$emit('copyModal', { id: id, show: this.showModal })
    },
    paginationClick(page) {
      this.$emit('clickPagination', { page: page })
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

<template>
  <v-container>
    <v-flex xs12 class="text-xs-center">
      <v-card>
        <v-card-title primary-title>
          <h3 class="headline mb-0">欢迎您，{{ user.username }}</h3>
        </v-card-title>

        <v-card-actions>
          <v-btn @click="logout" color="success">注销</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <v-divider class="mx-2"></v-divider>

    <div>
      <v-toolbar flat color="white">
        <v-toolbar-title>翻译历史</v-toolbar-title>
        <v-divider
            class="mx-2"
            inset
            vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-btn color="primary"
               dark class="mb-2"
               @click="getTranslationHistory()"
        >
          刷新
        </v-btn>
      </v-toolbar>
      <v-data-table
          :headers="headers"
          :items="transHistory"
          :search="search"
          class="elevation-1"
      >
        <template v-slot:items="props">
          <td>{{ props.item.source }}</td>
          <td class="text-xs-center">{{ props.item.target }}</td>
          <td class="text-xs-center">{{ props.item.created_at }}</td>
          <td class="">
            <v-icon
                small
                @click="deleteItem(props.item)"
            >
              delete
            </v-icon>
          </td>
        </template>
        <template v-slot:no-data>
          <v-alert :value="true" color="info" icon="warning">
            暂无记录
          </v-alert>
        </template>
        <template v-slot:no-results>
          <v-alert :value="true" color="info" icon="warning">
            没有找到匹配“{{ search }}”的记录
          </v-alert>
        </template>
      </v-data-table>
    </div>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import config from "@/config.ts";
  import {get, post} from "@/helpers.ts";
  import {mapState} from "vuex";

  export default Vue.extend({
    name: "register",
    data: () => ({
      dialog: false,
      search: "",
      headers: [
        {
          text: "原句",
          align: "center",
          sortable: false,
          value: "source"
        },
        {
          text: "翻译",
          align: "center",
          sortable: false,
          value: "target"
        },
        {
          text: "插入时间",
          align: "center",
          sortable: true,
          value: "created_at"
        },
        {text: "操作", value: "name", sortable: false}
      ],
      transHistory: [],
    }),
    computed: {
      ...mapState([
        "user",
      ]),
      formTitle() {
        return this.editedIndex === -1 ? "New Item" : "Edit Item";
      },
    },
    watch: {
      dialog(val) {
        val || this.close();
      }
    },
    created() {
      if (this.user.id === -1) {
        this.$router.push("/auth/login");
        return;
      }
      this.getTranslationHistory();
    },
    methods: {
      async logout() {
        const response = await get<{
          result: boolean,
          code: number,
          msg: string,
          data: any,
        }>(config.baseUrl + "auth/logout");
        // console.log(response.parsedBody);
        if (response.parsedBody.result) {
          this.$store.dispatch("logout");
          this.showInfo(response.parsedBody.msg);
          this.$router.push("/auth/login");
        } else {
          this.showError(response.parsedBody.msg);
        }
      },
      async getTranslationHistory() {
        const response = await get<{
          result: boolean,
          code: number,
          msg: string,
          data: any,
        }>(config.baseUrl + "translation/history");
        if (response.parsedBody.result) {
          this.transHistory = response.parsedBody.data;
        } else {
          this.showError(response.parsedBody.msg);
        }
      },
      async deleteTranslationHistory(id: number) {
        const response = await post<{
          result: boolean,
          code: number,
          msg: string,
          data: any,
        }>(config.baseUrl + "translation/history/delete",
          {
            "id": id,
          });
        if (response.parsedBody.result) {
          this.showInfo(response.parsedBody!.msg);
        } else {
          this.showError(response.parsedBody.msg);
        }
      },
      async deleteItem(item) {
        if (!confirm("确定要删除此条记录吗?")) {
          return;
        }
        await this.deleteTranslationHistory(item.id);
        await this.getTranslationHistory();
      },

      close() {
        this.dialog = false;
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem);
          this.editedIndex = -1;
        }, 300);
      },

      save() {
        if (this.editedIndex > -1) {
          Object.assign(this.transHistory[this.editedIndex], this.editedItem);
        } else {
          this.transHistory.push(this.editedItem);
        }
        this.close();
      },

      showInfo(msg: string) {
        this.$store.dispatch("showInfo", msg);
      },
      showError(msg: string) {
        this.$store.dispatch("showError", msg);
      },
    }
  });
</script>

<style scoped lang="stylus">

</style>

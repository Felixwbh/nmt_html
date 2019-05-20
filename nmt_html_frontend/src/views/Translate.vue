<template>
  <v-container>
    <v-tabs
        color="cyan"
        dark
        slider-color="yellow"
        grow
    >
      <v-tab ripple>单句翻译</v-tab>
      <v-tab-item>
        <v-container>
          <v-layout row wrap justify-center>
            <v-flex xs12>
              <v-text-field
                  v-model="srcSingle"
                  :error-messages="srcSingleErrors"
                  :label="translateSingleInputPlaceHolder"
                  required
                  @input="$v.srcSingle.$touch()"
                  @blur="$v.srcSingle.$touch()"
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                  v-model="translateSingleResult"
                  :label="translateSingleResultPlaceHolder"
                  readonly
              ></v-text-field>
            </v-flex>
            <transition name="fade">
              <v-flex xs12 v-show="srcSingleHasTag && translateSingleResult.length > 0">
                <v-text-field
                    v-model="alignSingleResult"
                    :label="translateSingleAlignPlaceHolder"
                    readonly
                ></v-text-field>
              </v-flex>
            </transition>

            <v-flex xs6 lg2>
              <v-switch
                  v-model="isSingleChToEn"
                  :label="isSingleChToEnSwitch"
              ></v-switch>
            </v-flex>
            <v-flex xs6 lg2>
              <v-switch
                  v-model="srcSingleHasTag"
                  :label="srcSingleHasTagSwitch"
              ></v-switch>
            </v-flex>

            <v-flex xs12>
              <v-btn @click="translateSingle" color="success">翻译</v-btn>
              <transition name="fade">
                <v-btn
                    @click="alignSingle"
                    dark color="blue"
                    v-show="srcSingleHasTag && translateSingleResult.length > 0"
                >
                  对齐
                </v-btn>
              </transition>
            </v-flex>
          </v-layout>
        </v-container>
      </v-tab-item>

      <v-tab ripple>页面翻译</v-tab>
      <v-tab-item>
        <v-container>
          <v-layout row wrap justify-center>
            <v-flex xs12>
              <v-textarea
                  v-model="srcPage"
                  :error-messages="srcPageErrors"
                  :label="translatePageInputPlaceHolder"
                  required
                  @input="$v.srcPage.$touch()"
                  @blur="$v.srcPage.$touch()"
              ></v-textarea>
            </v-flex>
            <v-flex xs12>
              <v-textarea
                  v-model="translatePageResult"
                  :label="translatePageResultPlaceHolder"
                  readonly
              ></v-textarea>
            </v-flex>

            <v-flex xs12>
              <v-switch
                  v-model="isPageChToEn"
                  :label="isPageChToEnSwitch"
              ></v-switch>
            </v-flex>

            <v-flex xs12>
              <v-btn @click="translatePage" color="success">翻译页面</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import {validationMixin} from "vuelidate";
  import {required, maxLength, minLength, sameAs} from "vuelidate/lib/validators";
  import config from "@/config.ts";
  import {get, post} from "@/helpers.ts";

  export default Vue.extend({
    mixins: [validationMixin],
    name: "translate",
    validations: {
      srcSingle: {required, maxLength: maxLength(1024)},
      srcPage: {required},
    },
    data: () => ({
      // Single
      srcSingle: "",
      translateSingleResult: "",
      alignSingleResult: "",
      srcSingleHasTag: false,
      isSingleChToEn: false,
      // Page
      srcPage: "",
      translatePageResult: "",
      isPageChToEn: false,
    }),
    computed: {
      // Single
      srcSingleHasTagSwitch() {
        if (this.srcSingleHasTag) {
          return "包含标签";
        } else {
          return "不包含标签";
        }
      },
      isSingleChToEnSwitch() {
        if (this.isSingleChToEn) {
          return "中译英";
        } else {
          return "英译中";
        }
      },
      srcSingleErrors() {
        const errors: any[] = [];
        if (!this.$v.srcSingle!.$dirty) {
          return errors;
        }
        if (this.isSingleChToEn) {
          !this.$v.srcSingle!.maxLength && errors.push("The length of the sentence cannot exceed 1024");
          !this.$v.srcSingle!.required && errors.push("Please input a sentence");
        } else {
          !this.$v.srcSingle!.maxLength && errors.push("句子长度不能超过 1024");
          !this.$v.srcSingle!.required && errors.push("请输入单句");
        }
        return errors;
      },
      translateSingleInputPlaceHolder() {
        if (this.isSingleChToEn) {
          return "Please input a sentence";
        } else {
          return "输入单句";
        }
      },
      translateSingleResultPlaceHolder() {
        if (this.isSingleChToEn) {
          return "Translation result";
        } else {
          return "翻译结果";
        }
      },
      translateSingleAlignPlaceHolder() {
        if (this.isSingleChToEn) {
          return "Align result";
        } else {
          return "对齐结果";
        }
      },
      translateSingleAPI() {
        if (this.isSingleChToEn) {
          if (this.srcSingleHasTag) {
            return "translatecetag";
          } else {
            return "translatece";
          }
        } else {
          if (this.srcSingleHasTag) {
            return "translateectag";
          } else {
            return "translateec";
          }
        }
      },
      // Page
      isPageChToEnSwitch() {
        if (this.isPageChToEn) {
          return "中译英";
        } else {
          return "英译中";
        }
      },
      srcPageErrors() {
        const errors: any[] = [];
        if (!this.$v.srcPage!.$dirty) {
          return errors;
        }
        if (this.isPageChToEn) {
          !this.$v.srcPage!.required && errors.push("Please input HTML");
        } else {
          !this.$v.srcPage!.required && errors.push("请输入 HTML");
        }
        return errors;
      },
      translatePageInputPlaceHolder() {
        if (this.isPageChToEn) {
          return "Please input HTML";
        } else {
          return "输入 HTML";
        }
      },
      translatePageResultPlaceHolder() {
        if (this.isPageChToEn) {
          return "Translation result";
        } else {
          return "翻译结果";
        }
      },
      translatePageAPI() {
        if (this.isPageChToEn) {
          return "translatehtml";
        } else {
          return "translatehtml";
        }
      },
    },
    methods: {
      async translateSingle() {
        this.$v.$touch();
        if (this.$v.srcSingle!.$invalid) {
          return;
        } else {
          this.translateSingleResult = "";
          const response = await post<{
            result: boolean,
            code: number,
            msg: string,
            data: string,
          }>(config.baseUrl + this.translateSingleAPI,
            {
              input: this.srcSingle,
            });
          // console.log(response.parsedBody);
          if (response.parsedBody!.result) {
            this.showInfo(response.parsedBody!.msg);
            // console.log(response.parsedBody.data);
            this.translateSingleResult = response.parsedBody.data;
          } else {
            this.showError(response.parsedBody!.msg);
          }
        }
      },
      async alignSingle() {
        this.$v.$touch();
        if (this.$v.srcSingle!.$invalid) {
          return;
        } else {
          const response = await post<{
            result: boolean,
            code: number,
            msg: string,
            data: string,
          }>(config.baseUrl + "align",
            {
              translation: this.translateSingleResult,
            });
          // console.log(response.parsedBody);
          if (response.parsedBody!.result) {
            this.showInfo(response.parsedBody!.msg);
            // console.log(response.parsedBody.data);
            this.alignSingleResult = response.parsedBody.data;
          } else {
            this.showError(response.parsedBody!.msg);
          }
        }
      },
      async translatePage() {
        this.$v.$touch();
        if (this.$v.srcPage!.$invalid) {
          return;
        } else {
          this.translatePageResult = "";
          const response = await post<{
            result: boolean,
            code: number,
            msg: string,
            data: string,
          }>(config.baseUrl + this.translatePageAPI,
            {
              input: this.srcPage,
            });
          // console.log(response.parsedBody);
          if (response.parsedBody!.result) {
            this.showInfo(response.parsedBody!.msg);
            // console.log(response.parsedBody.data);
            this.translatePageResult = response.parsedBody.data;
          } else {
            this.showError(response.parsedBody!.msg);
          }
        }
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
  .fade-enter-active, .fade-leave-active
    transition: opacity .5s

  .fade-enter, .fade-leave-to
    opacity: 0
</style>

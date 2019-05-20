<template>
  <v-container fill-height>
    <v-layout
        text-xs-center
        wrap
        fill-height
        justify-center
        align-content-center
    >
      <v-flex xs12>
        <v-img
            :src="require('../assets/nlplab.png')"
            class="my-3"
            contain
            height="100"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          欢迎使用神经网络机器翻译系统
        </h1>
        <p class="subheading font-weight-regular">
          为了获得更好的用户体验,
          <br>请
          <router-link to="/auth/register">注册并登录</router-link>
        </p>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
  import Vue from "vue";

  export default Vue.extend({
    data() {
      return {
        //
      }
    },
  });
</script>

<style>

</style>

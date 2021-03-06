<template>
  <v-container>
    <form>
      <v-text-field
          v-model="username"
          :error-messages="usernameErrors"
          label="用户名 (不超过 20 个字符)"
          required
          @input="$v.username.$touch()"
          @blur="$v.username.$touch()"
      ></v-text-field>
      <v-text-field
          v-model="password"
          :error-messages="passwordErrors"
          label="密码 (6 - 20)"
          type="password"
          required
          @input="$v.password.$touch()"
          @blur="$v.password.$touch()"
      ></v-text-field>
      <v-text-field
          v-model="rePassword"
          :error-messages="rePasswordErrors"
          label="确认密码 (6 - 20)"
          type="password"
          required
          @input="$v.rePassword.$touch()"
          @blur="$v.rePassword.$touch()"
      ></v-text-field>

      <v-btn @click="submit" color="success">注册</v-btn>
      <v-btn @click="clear" color="warning">重置表单</v-btn>
    </form>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import {validationMixin} from "vuelidate";
  import {required, maxLength, minLength, sameAs} from "vuelidate/lib/validators";
  import config from "@/config.ts";
  import {post} from "@/helpers.ts";

  export default Vue.extend({
    mixins: [validationMixin],
    name: "register",
    validations: {
      username: {required, maxLength: maxLength(20)},
      password: {required, minLength: minLength(6), maxLength: maxLength(20)},
      rePassword: {required, sameAsPassword: sameAs("password")},
    },
    data: () => ({
      username: "",
      password: "",
      rePassword: "",
    }),
    computed: {
      usernameErrors() {
        const errors: any[] = [];
        if (!this.$v.username!.$dirty) {
          return errors;
        }
        !this.$v.username!.maxLength && errors.push("用户名长度不能超过 20");
        !this.$v.username!.required && errors.push("请输入用户名");
        return errors;
      },
      passwordErrors() {
        const errors: any = [];
        if (!this.$v.password!.$dirty) {
          return errors;
        }
        !this.$v.password!.minLength && errors.push("密码长度必须大于 6");
        !this.$v.password!.maxLength && errors.push("密码长度必须小于 20");
        !this.$v.password!.required && errors.push("请输入密码");
        return errors;
      },
      rePasswordErrors() {
        const errors: any[] = [];
        if (!this.$v.rePassword!.$dirty) {
          return errors;
        }
        !this.$v.rePassword!.sameAsPassword && errors.push("两次输入的密码不一致");
        !this.$v.rePassword!.required && errors.push("请再次输入密码");
        return errors;
      },
    },
    methods: {
      async submit() {
        this.$v.$touch();
        if (this.$v.$invalid) {
          return;
        } else {
          const response = await post<{
            result: boolean,
            code: number,
            msg: string,
            data: any,
          }>(config.baseUrl + "auth/register",
            {
              username: this.username,
              password: this.password,
              rePassword: this.rePassword,
            });
          // console.log(response.parsedBody);
          if (response.parsedBody!.result) {
            this.showInfo(response.parsedBody!.msg + "，请登录");
            this.$router.push("/auth/login");
          } else {
            this.showError(response.parsedBody!.msg);
          }

        }
      },
      clear() {
        this.$v.$reset();
        this.username = "";
        this.password = "";
        this.rePassword = "";
      },
      showInfo(msg: string) {
        this.$store.dispatch('showInfo', msg);
      },
      showError(msg: string) {
        this.$store.dispatch('showError', msg);
      },
    }
  });
</script>

<style scoped lang="stylus">

</style>

const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack');

module.exports = defineConfig({
  publicPath: process.env.NODE_ENV === "production" ? "/HarmonicAI/" : "/",
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      }),
    ],
  },
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/sass/index.scss";`
      },
    },
  },
})

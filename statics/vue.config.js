const {defineConfig} = require('@vue/cli-service')
// module.exports = defineConfig({
//     transpileDependencies: true,
//     runtimeCompiler: true,
//     // filenameHashing: false,
//     configureWebpack: {
//         devtool: 'source-map',
//     },
//     devServer: {
//         allowedHosts: "all",
//     }
// })

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },
};

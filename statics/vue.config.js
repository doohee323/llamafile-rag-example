const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    runtimeCompiler: true,
    // filenameHashing: false,
    configureWebpack: {
        devtool: 'source-map',
    },
    devServer: {
        allowedHosts: "all",
    }
})

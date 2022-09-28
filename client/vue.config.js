const {defineConfig} = require('@vue/cli-service')
const path = require("path");
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const {ElementPlusResolver} = require('unplugin-vue-components/resolvers')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const CompressionWebpackPlugin = require('compression-webpack-plugin');

const title = 'xshare'
const version='2.3.8';

const pro_base_env = {
    baseUrl: '/',       //该选项可以填写web-api的域名，类似 https://api.xxx.com/
    static: '/',  //若配置cdn等加速，可以填写cdn加速域名
    version: version,
};
const footer_info = {
    copyright: 'Copyright © 2022-2099 isummer 版权所有.',
    ipcBeiAn: {
        url: 'https://beian.miit.gov.cn',
        text: '京ICP备668686886号',
    },
    gongAnBeiAn: {
        url: 'https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=98868998',
        text: '京公网安备98868998号',
    },
}
function resolve(dir) {
    return path.join(__dirname, dir)
}

const compress = new CompressionWebpackPlugin(
    {
        algorithm: 'gzip',
        threshold: 10240,
        test: new RegExp(
            '\\.(' +
            ['js', 'css'].join('|') +
            ')$'
        ),
        minRatio: 0.8,
        deleteOriginalAssets: false
    }
);

module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: pro_base_env.static,
    outputDir: 'dist',
    assetsDir: 'static',
    productionSourceMap: false,
    configureWebpack: {
        // provide the app's title in webpack's name field, so that
        // it can be accessed in index.html to inject the correct title.
        name: title,
        resolve: {
            alias: {
                '@': resolve('src')
            }
        },
        plugins: [compress,
            AutoImport({
                resolvers: [ElementPlusResolver()],
            }),
            Components({
                resolvers: [ElementPlusResolver()],
            }),
        ]
    },
    chainWebpack(config) {

        // when there are many pages, it will cause too many meaningless requests
        config.plugins.delete('prefetch')
        config.plugin('html').tap(args => {
            args[0].title = title
            return args
        })
        config
            .plugin('define')
            .tap(args => {
                args[0]['process.env']['base_env'] = JSON.stringify({
                    baseUrl: pro_base_env.baseUrl,
                    version: pro_base_env.version,
                    footer: footer_info
                });
                return args
            });
        config.plugins.delete('preload');

        config.optimization.minimizer = [
            new UglifyJsPlugin({
                uglifyOptions: {
                    output: {
                        comments: false, // 去掉注释
                    },
                    warnings: false,
                    compress: {
                        drop_console: true,
                        drop_debugger: true,
                        pure_funcs: ['console.log']//移除console
                    }
                }
            })
        ]
        config
            .when(process.env.NODE_ENV !== 'development',
                config => {
                    config
                        .plugin('ScriptExtHtmlWebpackPlugin')
                        .after('html')
                        .use('script-ext-html-webpack-plugin', [{
                            // `runtime` must same as runtimeChunk name. default is `runtime`
                            inline: /runtime\..*\.js$/
                        }])
                        .end()
                    config
                        .optimization.splitChunks({
                        chunks: 'all',
                        cacheGroups: {
                            libs: {
                                name: 'chunk-libs',
                                test: /[\\/]node_modules[\\/]/,
                                priority: 10,
                                chunks: 'initial' // only package third parties that are initially dependent
                            },
                            elementUI: {
                                name: 'chunk-elementUI', // split elementUI into a single package
                                priority: 20, // the weight needs to be larger than libs and app or it will be packaged into libs or app
                                test: /[\\/]node_modules[\\/]_?element-plus(.*)/ // in order to adapt to cnpm
                            },
                            commons: {
                                name: 'chunk-commons',
                                test: resolve('src/components'), // can customize your rules
                                minChunks: 3, //  minimum common number
                                priority: 5,
                                reuseExistingChunk: true
                            }
                        }
                    })
                    // https:// webpack.js.org/configuration/optimization/#optimizationruntimechunk
                    config.optimization.runtimeChunk('single')
                }
            )
    }
})

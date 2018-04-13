const path = require('path')

module.exports = {
    output: {
        filename: '[name].js',
        path: __dirname+"/public"
    },
    entry:{
        'client':'./www-src/client.ts'
    },
    resolve: {
        modules: [
            'node_modules',
            path.join(__dirname, 'node_modules')
        ],
        extensions: ['.ts', '.tsx', '.js', '.jsx']
      },
    module: {
        rules: [
            {
                test:/\.tsx?$/,
                loader:"awesome-typescript-loader",
                exclude:/node_modules/
            }
        ]
    }
    
}
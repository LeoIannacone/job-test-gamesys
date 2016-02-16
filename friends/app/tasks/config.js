import path from 'path'

const dist = path.join(__dirname, '..', '..', '..', 'static', 'dist')

const webpackConfig = {
  entry: path.join(__dirname, '..', 'scripts', 'main.js'),
  output: {
    path: dist,
    filename: 'app.js'
  },
  module: {
    loaders: [
      {
        test: /.js?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'react']
        }
      }
    ]
  }
}

export default {
  webpackConfig,
  dist
}

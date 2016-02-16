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
  dist,
  browsers: [
    'ie >= 10',
    'ie_mob >= 10',
    'ff >= 30',
    'chrome >= 34',
    'safari >= 6',
    'opera >= 23',
    'ios >= 6',
    'android >= 4.4',
    'bb >= 10'
  ]
}

'use strict';
var path = require('path');
var webpack = require('webpack');

module.exports = {
  resolve: {
    extensions: ['', '.js'],
    modulesDirectories: ['node_modules', 'src'],
  },
  entry: {
    app: [
      'webpack-dev-server/client?http://0.0.0.0:3000',
      'webpack/hot/only-dev-server',
      './src/client.jsx' // Your appʼs entry point
    ]
  },
  output: {
    path: path.join(__dirname, 'public'),
    publicPath: '/public/',
    filename: 'client.js',
  },
  module: {
    loaders: [
      {test: /\.jsx?$/, exclude: /node_modules/, loaders:
        ['react-hot', 'babel-loader?stage=0&optional=runtime']},

      {test: /\.less$/, loader: 'style-loader!css-loader!autoprefixer-loader?{browsers:["last 2 version"]}!less-loader'},

      {test: /\.(?:eot|ttf|woff2?)$/, loader: 'file-loader?name=[path][name]-[hash:6].[ext]&context=assets'}
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new webpack.ProvidePlugin({
      Radium: 'radium', Flummox: 'flummox', m: 'mori'
    })

  ],
  devtool: 'eval-source-map'
};

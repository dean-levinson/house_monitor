const path = require('path');

module.exports = {
    entry: path.join(__dirname, 'client', 'index.js'),
    output: {
        path: path.join(__dirname, 'public', 'dist'),
        filename: 'bundle.js'
    },
    mode: 'development',
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        },
        {
          test:  /\.css$/,
          exclude: /node_modules/,
          use: ["style-loader", "css-loader"]
        },
        {
          test:  /\.(jpg|png)$/,
          exclude: /node_modules/,
          use: ["url-loader"]
        }
      ]
    }
  };
const { defineConfig } = require("@vue/cli-service");
module.exports = {
  lintOnSave: false, // Отключаем линтинг при сохранении
  devServer: {
    hot: false, // Отключаем горячую перезагрузку
    liveReload: false, // Отключаем автообновление страниц
    watchFiles: {
      paths: ["src/**/*", "public/**/*"],
      options: {
        ignored: /node_modules/,
      },
    },
  },
  configureWebpack: {
    devtool: "source-map", // Для отладки
  },
};

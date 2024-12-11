const CracoLessPlugin = require('craco-less');

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: { '@primary-color': '#1DA57A' },  // Променете основния цвят
            javascriptEnabled: true,                       // Включете възможността за JavaScript в Less
          },
        },
      },
    },
  ],
};

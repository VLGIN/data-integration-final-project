import { createApp } from 'vue';
import App from './App.vue';
import plugins from './plugins';
import './assets/styles/global.scss';

const app = createApp(App)
  .use(plugins.router)
  .use(plugins.i18n)
  .use(plugins.ElementUI)
  .use(plugins.pinia);

app.mount('#app');

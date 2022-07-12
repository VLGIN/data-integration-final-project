import { createRouter, createWebHistory } from 'vue-router';
import i18n from '@/plugins/vue-i18n';

import { PageName } from '@/common/constants';
import MainLayout from '@/layout/MainLayout.vue';
import HomePage from '@/pages/home/HomePage.vue';
import ProductPage from '@/pages/product/ProductPage.vue';

const { t } = i18n.global;

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '/',
        name: PageName.HOME_PAGE,
        component: HomePage,
        meta: {
          title: t('app.title.home'),
        },
      },
      {
        path: '/home',
        redirect: '/',
      },
      {
        path: '/product',
        name: PageName.PRODUCT_PAGE,
        component: ProductPage,
        meta: {
          title: t('app.title.product'),
        },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;

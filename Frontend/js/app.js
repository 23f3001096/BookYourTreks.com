// ============================================
// js/app.js
// ============================================
const app = Vue.createApp({
    template: `<router-view />`
});

// Global components register kar — taaki har page/layout mein direct use ho sake
app.component('navbar', Navbar);
app.component('sidebar', Sidebar);
app.component('stat-card', StatCard);
app.component('status-badge', StatusBadge);
app.component('trek-card', TrekCard);
app.component('loading-spinner', LoadingSpinner);

app.use(router);
app.mount('#app');
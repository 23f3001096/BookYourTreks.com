const routes = [
    { path: '/', component: Landing },
    { path: '/login', component: Login },
    { path: '/register', component: Register },

    {
    path: '/admin', component: AdminLayout, meta: { role: 'admin' },
    children: [
        { path: 'dashboard', component: AdminDashboard },
        { path: 'treks', component: ManageTreks },
        { path: 'treks/:id/trekkers', component: TrekTrekkers },
        { path: 'staff', component: ManageStaff },
        { path: 'users', component: ManageUsers },
        { path: 'bookings', component: AllBookings },
        { path: 'reports', component: AdminStats },     // <-- ye line honi chahiye
        { path: 'profile', component: AdminProfile },
    ]
},
    {
    path: '/staff', component: StaffLayout, meta: { role: 'staff' },
    children: [
        { path: 'dashboard', component: StaffDashboard },
        { path: 'treks', component: MyTreks },
        { path: 'treks/:id', component: StaffTrekDetail },
        { path: 'profile', component: StaffProfile },
    ]
},
    {
    path: '/customer', component: CustomerLayout, meta: { role: 'customer' },
    children: [
        { path: 'dashboard', component: CustomerDashboard },
        { path: 'treks', component: TrekList },
        { path: 'treks/:id', component: TrekDetails },
        { path: 'bookings', component: MyBookings },
        { path: 'history', component: History },
        { path: 'profile', component: Profile },
    ]
    },
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const requiredRole = to.meta.role;
    if (!requiredRole) return next();

    try {
        const res = await api.me();
        if (res.data.role === requiredRole) next();
        else next('/login');
    } catch (err) {
        next('/login');
    }
});
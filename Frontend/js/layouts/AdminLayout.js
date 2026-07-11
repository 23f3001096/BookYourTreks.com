const AdminLayout = {
    template: `
        <div>
            <navbar role="admin" :userName="userName"></navbar>
            <div class="d-flex">
                <sidebar :items="menuItems"></sidebar>
                <div class="flex-grow-1 p-4">
                    <router-view />
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            userName: '',
            menuItems: [
    { path: '/admin/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
    { path: '/admin/treks', label: 'Treks', icon: 'bi bi-map' },
    { path: '/admin/staff', label: 'Staff', icon: 'bi bi-person-badge' },
    { path: '/admin/users', label: 'Users', icon: 'bi bi-people' },
    { path: '/admin/bookings', label: 'Bookings', icon: 'bi bi-journal-check' },
    { path: '/admin/reports', label: 'Reports', icon: 'bi bi-graph-up' },   // <-- ye line honi chahiye
    { path: '/admin/profile', label: 'Profile', icon: 'bi bi-person-circle' },
],
        };
    },
    async mounted() {
        const res = await api.me();
        this.userName = res.data.name;
    }
};
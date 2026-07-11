const CustomerLayout = {
    template: `
        <div>
            <navbar role="customer" :userName="userName"></navbar>
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
                { path: '/customer/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
                { path: '/customer/treks', label: 'Browse Treks', icon: 'bi bi-map' },
                { path: '/customer/bookings', label: 'My Bookings', icon: 'bi bi-journal-check' },
                { path: '/customer/history', label: 'History', icon: 'bi bi-clock-history' },
                { path: '/customer/profile', label: 'Profile', icon: 'bi bi-person' },
            ]
        };
    },
    async mounted() {
        const res = await api.me();
        this.userName = res.data.name;
    }
};
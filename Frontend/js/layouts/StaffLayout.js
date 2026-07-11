const StaffLayout = {
    template: `
        <div>
            <navbar role="staff" :userName="userName"></navbar>
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
                { path: '/staff/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
                { path: '/staff/treks', label: 'My Treks', icon: 'bi bi-map' },
                { path: '/staff/profile', label: 'Profile', icon: 'bi bi-person-circle' }
            ]
        };
    },
    async mounted() {
        const res = await api.me();
        this.userName = res.data.name;
    }
};
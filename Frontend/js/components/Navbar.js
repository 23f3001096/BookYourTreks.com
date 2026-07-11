const Navbar = {
    props: ['role', 'userName'],
    template: `
        <nav class="navbar navbar-expand-lg navbar-brand-custom shadow-sm px-4">
            <router-link class="navbar-brand fw-bold text-white" to="/">
                <i class="bi bi-tree-fill"></i> BookYourTreks
            </router-link>
            <div class="ms-auto d-flex align-items-center gap-5">
                <span class="text-white fw-bold"><i class="bi bi-person-circle"></i> {{ userName.toUpperCase() }}</span>
                <button class="btn btn-light fw-bold btn-sm" @click="logout">Logout</button>
            </div>
        </nav>
    `,
    methods: {
        async logout() {
            await api.logout();
            this.$router.push('/login');
        }
    }
};
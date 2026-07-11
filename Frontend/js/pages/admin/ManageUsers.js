const ManageUsers = {
    template: `
        <div>
            <h3 class="text-brand mb-3">Manage Users</h3>

            <div class="input-group mb-3" style="max-width:400px">
                <input v-model="searchQuery" class="form-control" placeholder="Search users..." @keyup.enter="search" />
                <button class="btn btn-outline-secondary" @click="search"><i class="bi bi-search"></i></button>
                <button class="btn btn-outline-secondary" @click="clearSearch" v-if="searched"><i class="bi bi-x"></i></button>
            </div>

            <loading-spinner v-if="loading"></loading-spinner>
            <table v-else class="table table-hover bg-white rounded shadow-sm align-middle">
                <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                    <tr v-for="u in users" :key="u.id">
                        <td>{{ u.id }}</td><td>{{ u.name }}</td><td>{{ u.email }}</td>
                        <td>
                            <span class="badge" :class="u.blocked ? 'bg-danger' : (u.active ? 'bg-success' : 'bg-secondary')">
                                {{ u.blocked ? 'Blocked' : (u.active ? 'Active' : 'Deactivated') }}
                            </span>
                        </td>
                        <td class="d-flex gap-2">
                            <button v-if="!u.blocked" class="btn btn-sm btn-outline-danger" @click="blockUser(u.id)">Block</button>
                            <button v-else class="btn btn-sm btn-outline-success" @click="activateUser(u.id)">Unblock</button>
                        </td>
                    </tr>
                    <tr v-if="users.length === 0"><td colspan="5" class="text-center text-muted py-3">No users found</td></tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return { users: [], loading: true, searchQuery: '', searched: false };
    },
    async mounted() { await this.loadUsers(); },
    methods: {
        async loadUsers() {
            this.loading = true;
            const res = await api.listUsers();
            this.users = res.data;
            this.loading = false;
        },
        async blockUser(id) {
            try {
                await api.blockUser(id);
                await this.loadUsers();
            } catch (err) { alert(err.message); }
        },
        async activateUser(id) {
            try {
                await api.activateUser(id);
                await this.loadUsers();
            } catch (err) { alert(err.message); }
        },
        async search() {
            if (!this.searchQuery.trim()) return;
            this.loading = true;
            const res = await api.searchUsers(this.searchQuery);
            this.users = res.data;
            this.searched = true;
            this.loading = false;
        },
        async clearSearch() {
            this.searchQuery = '';
            this.searched = false;
            await this.loadUsers();
        }
    }
};
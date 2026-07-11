const ManageTreks = {
    template: `
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="text-brand mb-0">Manage Treks</h3>
                <button class="btn btn-primary" @click="openCreateForm">
                    <i class="bi bi-plus-lg"></i> Add Trek
                </button>
            </div>

            <div class="input-group mb-3" style="max-width:400px">
                <input v-model="searchQuery" class="form-control" placeholder="Search treks..." @keyup.enter="search" />
                <button class="btn btn-outline-secondary" @click="search"><i class="bi bi-search"></i></button>
                <button class="btn btn-outline-secondary" @click="clearSearch" v-if="searched"><i class="bi bi-x"></i></button>
            </div>

            <!-- Create/Edit Form -->
            <div v-if="showForm" class="card p-4 mb-4 shadow-sm">
                <h5 class="mb-3">{{ editingId ? 'Edit Trek' : 'Create New Trek' }}</h5>
                <form @submit.prevent="submitForm" class="row g-3">
                    <div class="col-md-4">
                        <label class="form-label">Trek Name</label>
                        <input v-model="form.name" class="form-control" placeholder="e.g. Everest Base Camp" required />
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">Location</label>
                        <input v-model="form.location" class="form-control" placeholder="e.g. Nepal" required />
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">Difficulty</label>
                        <select v-model="form.difficulty" class="form-select" required>
                            <option value="" disabled>Select difficulty</option>
                            <option value="easy">Easy</option>
                            <option value="moderate">Moderate</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>

                    <div class="col-md-3">
                        <label class="form-label">Duration (days)</label>
                        <input v-model.number="form.duration_days" type="number" min="1" class="form-control" required />
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Available Slots</label>
                        <input v-model.number="form.available_slots" type="number" min="0" class="form-control" required />
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Start Date</label>
                        <input v-model="form.start_date" type="date" class="form-control" required />
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">End Date</label>
                        <input v-model="form.end_date" type="date" class="form-control" required />
                    </div>

                    <div v-if="formError" class="col-12">
                        <div class="alert alert-danger py-2 mb-0">{{ formError }}</div>
                    </div>

                    <div class="col-12 d-flex gap-2 mt-2">
                        <button class="btn btn-primary" type="submit" :disabled="saving">
                            {{ saving ? 'Saving...' : (editingId ? 'Update Trek' : 'Create Trek') }}
                        </button>
                        <button class="btn btn-outline-secondary" type="button" @click="cancelForm">Cancel</button>
                    </div>
                </form>
            </div>

            <loading-spinner v-if="loading"></loading-spinner>
            <table v-else class="table table-hover bg-white rounded shadow-sm align-middle">
                <thead>
                    <tr>
                        <th>ID</th><th>Name</th><th>Location</th><th>Difficulty</th>
                        <th>Slots</th><th>Status</th><th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="trek in treks" :key="trek.id">
                        <td>{{ trek.id }}</td>
                        <td>{{ trek.name }}</td>
                        <td>{{ trek.location }}</td>
                        <td class="text-capitalize">{{ trek.difficulty }}</td>
                        <td>{{ trek.available_slots }}</td>
                        <td>
                            <select class="form-select form-select-sm" style="width:130px"
                                :value="trek.status" @change="changeStatus(trek.id, $event.target.value)">
                                <option value="pending">Pending</option>
                                <option value="approved">Approved</option>
                                <option value="open">Open</option>
                                <option value="closed">Closed</option>
                                <option value="completed">Completed</option>
                            </select>
                        </td>
                        <td class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-primary" @click="openEditForm(trek)" title="Edit">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" @click="removeTrek(trek.id)" title="Delete">
                                <i class="bi bi-trash"></i>
                            </button>
                            <router-link :to="'/admin/treks/' + trek.id + '/trekkers'" class="btn btn-sm btn-outline-secondary" title="View Trekkers">
                                <i class="bi bi-people"></i>
                            </router-link>
                        </td>
                    </tr>
                    <tr v-if="treks.length === 0">
                        <td colspan="7" class="text-center text-muted py-4">No treks found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return {
            treks: [], loading: true, showForm: false, editingId: null, saving: false, formError: '',
            searchQuery: '', searched: false,
            form: { name: '', location: '', difficulty: '', duration_days: null, available_slots: null, start_date: '', end_date: '' }
        };
    },
    async mounted() {
        await this.loadTreks();
    },
    methods: {
        async loadTreks() {
            this.loading = true;
            const res = await api.listTreks();
            this.treks = res.data;
            this.loading = false;
        },
        openCreateForm() {
            this.editingId = null;
            this.formError = '';
            this.form = { name: '', location: '', difficulty: '', duration_days: null, available_slots: null, start_date: '', end_date: '' };
            this.showForm = true;
        },
        openEditForm(trek) {
            this.editingId = trek.id;
            this.formError = '';
            this.form = {
                name: trek.name, location: trek.location, difficulty: trek.difficulty,
                duration_days: trek.duration_days, available_slots: trek.available_slots,
                start_date: trek.start_date, end_date: trek.end_date
            };
            this.showForm = true;
        },
        cancelForm() {
            this.showForm = false;
            this.editingId = null;
            this.formError = '';
        },
        async submitForm() {
            this.formError = '';
            this.saving = true;
            try {
                if (this.editingId) {
                    await api.editTrek(this.editingId, this.form);
                } else {
                    await api.createTrek(this.form);
                }
                this.showForm = false;
                this.editingId = null;
                await this.loadTreks();
            } catch (err) {
                this.formError = err.message;
            } finally {
                this.saving = false;
            }
        },
        async removeTrek(id) {
            if (!confirm('Delete this trek?')) return;
            try {
                await api.deleteTrek(id);
                await this.loadTreks();
            } catch (err) {
                alert(err.message);
            }
        },
        async changeStatus(id, status) {
            try {
                await api.updateTrekStatus(id, status);
                await this.loadTreks();
            } catch (err) {
                alert(err.message);
            }
        },
        async search() {
            if (!this.searchQuery.trim()) return;
            this.loading = true;
            const res = await api.searchTreks(this.searchQuery);
            this.treks = res.data;
            this.searched = true;
            this.loading = false;
        },
        async clearSearch() {
            this.searchQuery = '';
            this.searched = false;
            await this.loadTreks();
        }
    }
};
const ManageStaff = {
    template: `
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="text-brand mb-0">Manage Staff</h3>
                <button class="btn btn-primary" @click="openCreateForm">
                    <i class="bi bi-plus-lg"></i> Add Staff
                </button>
            </div>

            <div class="input-group mb-3" style="max-width:400px">
                <input v-model="searchQuery" class="form-control" placeholder="Search staff..." @keyup.enter="search" />
                <button class="btn btn-outline-secondary" @click="search"><i class="bi bi-search"></i></button>
                <button class="btn btn-outline-secondary" @click="clearSearch" v-if="searched"><i class="bi bi-x"></i></button>
            </div>

            <!-- Add Staff Form -->
            <div v-if="showForm" class="card p-4 mb-4 shadow-sm">
                <h5 class="mb-3">Create New Staff</h5>
                <form @submit.prevent="addStaff" class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label">Full Name</label>
                        <input v-model="form.name" class="form-control" placeholder="e.g. Vikram Kumar" required />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Email Address</label>
                        <input v-model="form.email" type="email" class="form-control" placeholder="e.g. vikram@gmail.com" required />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Password</label>
                        <input v-model="form.password" type="password" class="form-control" placeholder="Temporary password" required />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Contact Number</label>
                        <input v-model="form.contact_number" class="form-control" placeholder="e.g. 9876543210" required />
                    </div>

                    <div v-if="formError" class="col-12">
                        <div class="alert alert-danger py-2 mb-0">{{ formError }}</div>
                    </div>

                    <div class="col-12 d-flex gap-2 mt-2">
                        <button class="btn btn-primary" type="submit" :disabled="saving">
                            {{ saving ? 'Creating...' : 'Create Staff' }}
                        </button>
                        <button class="btn btn-outline-secondary" type="button" @click="cancelForm">Cancel</button>
                    </div>
                </form>
            </div>

            <!-- Assign Trek Form -->
            <div v-if="assigningStaffId" class="card p-4 mb-4 shadow-sm border-primary">
                <h5 class="mb-3">Assign Trek</h5>
                <div class="row g-3 align-items-end">
                    <div class="col-md-8">
                        <label class="form-label">Select Trek</label>
                        <select v-model="selectedTrekId" class="form-select">
                            <option value="" disabled>Choose a trek</option>
                            <option v-for="t in allTreks" :key="t.id" :value="t.id">
                                {{ t.name }} — {{ t.location }}
                            </option>
                        </select>
                    </div>
                    <div class="col-md-4 d-flex gap-2">
                        <button class="btn btn-primary" @click="confirmAssign">Assign</button>
                        <button class="btn btn-outline-secondary" @click="assigningStaffId = null">Cancel</button>
                    </div>
                </div>
            </div>

            <loading-spinner v-if="loading"></loading-spinner>
            <table v-else class="table table-hover bg-white rounded shadow-sm align-middle">
                <thead>
                    <tr>
                        <th>ID</th><th>Name</th><th>Contact</th><th>Status</th>
                        <th>Assigned Treks</th><th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="s in staffList" :key="s.id">
                        <td>{{ s.id }}</td>
                        <td>{{ s.name }}</td>
                        <td>{{ s.contact_number }}</td>
                        <td><status-badge :status="s.status"></status-badge></td>
                        <td>{{ s.assigned_treks }}</td>
                        <td class="d-flex gap-2 flex-wrap">
                            <button class="btn btn-sm btn-outline-primary" @click="openAssignForm(s.id)">
                                Assign Trek
                            </button>
                            <button v-if="s.status === 'active'" class="btn btn-sm btn-outline-danger" @click="blockStaff(s.id)">
                                Block
                            </button>
                            <button v-else class="btn btn-sm btn-outline-success" @click="activateStaff(s.id)">
                                Unblock
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" @click="removeStaff(s.id)" title="Remove">
                                <i class="bi bi-trash"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="staffList.length === 0">
                        <td colspan="6" class="text-center text-muted py-4">No staff found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return {
            staffList: [], loading: true, showForm: false, saving: false, formError: '',
            searchQuery: '', searched: false,
            form: { name: '', email: '', password: '', contact_number: '' },
            assigningStaffId: null, selectedTrekId: '', allTreks: []
        };
    },
    async mounted() {
        await this.loadStaff();
    },
    methods: {
        async loadStaff() {
            this.loading = true;
            const res = await api.listStaff();
            this.staffList = res.data;
            this.loading = false;
        },
        openCreateForm() {
            this.formError = '';
            this.form = { name: '', email: '', password: '', contact_number: '' };
            this.showForm = true;
        },
        cancelForm() {
            this.showForm = false;
            this.formError = '';
        },
        async addStaff() {
            this.formError = '';
            this.saving = true;
            try {
                await api.addStaff(this.form);
                this.showForm = false;
                this.form = { name: '', email: '', password: '', contact_number: '' };
                await this.loadStaff();
            } catch (err) {
                this.formError = err.message;
            } finally {
                this.saving = false;
            }
        },
        async blockStaff(id) {
            try { await api.blockStaff(id); await this.loadStaff(); }
            catch (err) { alert(err.message); }
        },
        async activateStaff(id) {
            try { await api.activateStaff(id); await this.loadStaff(); }
            catch (err) { alert(err.message); }
        },
        async removeStaff(id) {
            if (!confirm('Remove this staff member?')) return;
            try { await api.removeStaff(id); await this.loadStaff(); }
            catch (err) { alert(err.message); }
        },
        async search() {
            if (!this.searchQuery.trim()) return;
            this.loading = true;
            const res = await api.searchStaff(this.searchQuery);
            this.staffList = res.data;
            this.searched = true;
            this.loading = false;
        },
        async clearSearch() {
            this.searchQuery = '';
            this.searched = false;
            await this.loadStaff();
        },
        async openAssignForm(staffId) {
            this.assigningStaffId = staffId;
            this.selectedTrekId = '';
            const res = await api.listTreks();
            this.allTreks = res.data;
        },
        async confirmAssign() {
            if (!this.selectedTrekId) return alert('Please select a trek first');
            try {
                await api.assignStaffToTrek(this.assigningStaffId, this.selectedTrekId);
                alert('Trek assigned successfully!');
                this.assigningStaffId = null;
                await this.loadStaff();
            } catch (err) {
                alert(err.message);
            }
        }
    }
};
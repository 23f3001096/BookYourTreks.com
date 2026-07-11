const AdminProfile = {
    template: `
        <div>
            <h3 class="text-brand mb-3">My Profile</h3>
            <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">{{ message }}</div>
            <loading-spinner v-if="loading"></loading-spinner>
            <div v-else class="card p-4" style="max-width:450px">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input :value="profile.email" class="form-control" disabled />
                </div>
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="name" class="form-control" />
                </div>
                <button class="btn btn-primary" @click="save" :disabled="saving">
                    {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
            </div>
        </div>
    `,
    data() {
        return { profile: {}, name: '', loading: true, saving: false, message: '', messageType: 'success' };
    },
    async mounted() {
        const res = await api.adminProfile();
        this.profile = res.data;
        this.name = res.data.name;
        this.loading = false;
    },
    methods: {
        async save() {
            this.saving = true;
            this.message = '';
            try {
                await api.adminEditProfile({ name: this.name });
                this.message = 'Profile updated successfully';
                this.messageType = 'success';
            } catch (err) {
                this.message = err.message;
                this.messageType = 'danger';
            } finally {
                this.saving = false;
            }
        }
    }
};
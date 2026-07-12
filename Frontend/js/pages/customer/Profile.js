const Profile = {
    template: `
        <div>
            <h3 class="text-brand mb-3">My Profile</h3>
            <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">{{ message }}</div>
            <loading-spinner v-if="loading"></loading-spinner>
            <div v-else class="card p-4" style="max-width:450px">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input :value="email" class="form-control" disabled />
                </div>
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="form.name" class="form-control" />
                </div>
                <div class="mb-3">
                    <label class="form-label">Contact Number</label>
                    <input v-model="form.contact_number" class="form-control" />
                </div>
                <div class="mb-3">
                    <label class="form-label">Emergency Contact</label>
                    <input v-model="form.emergency_contact" class="form-control" />
                </div>
                <button class="btn btn-primary" @click="save" :disabled="saving">
                    {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
            </div>
        </div>
    `,
    data() {
        return {
            email: '',
            form: { name: '', contact_number: '', emergency_contact: '' },
            loading: true, saving: false, message: '', messageType: 'success'
        };
    },
    async mounted() {
        const meRes = await api.me();
        this.email = meRes.data.email;

        const res = await api.customerProfile();
        this.form = {
            name: res.data.name,
            contact_number: res.data.contact_number,
            emergency_contact: res.data.emergency_contact
        };
        this.loading = false;
    },
    methods: {
        async save() {
            this.saving = true;
            this.message = '';
            try {
                await api.customerEditProfile(this.form);
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
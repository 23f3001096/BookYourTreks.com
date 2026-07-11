const Register = {
    template: `
        <div class="d-flex justify-content-center align-items-center hero-section" style="min-height: 100vh;">
            <div class="card p-4 shadow" style="width: 400px;">
                <h4 class="mb-3 text-center text-brand"><i class="bi bi-person-plus"></i> Register</h4>
                <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
                <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
                <form @submit.prevent="handleRegister">
                    <div class="mb-2">
                        <label class="form-label">Full Name</label>
                        <input v-model="name" type="text" class="form-control" required />
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" required />
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" required />
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Contact Number</label>
                        <input v-model="contact_number" type="text" class="form-control" />
                    </div>
                    <button type="submit" class="btn btn-primary w-100 mt-2" :disabled="loading">
                        {{ loading ? 'Registering...' : 'Register' }}
                    </button>
                </form>
                <p class="text-center mt-3 mb-0">
                    Already have an account? <router-link to="/login">Login</router-link>
                </p>
            </div>
        </div>
    `,
    data() {
        return { name: '', email: '', password: '', contact_number: '', error: '', success: '', loading: false };
    },
    methods: {
        async handleRegister() {
            this.error = '';
            this.loading = true;
            try {
                await api.register({
                    name: this.name,
                    email: this.email,
                    password: this.password,
                    contact_number: this.contact_number
                });
                this.success = 'Registered! Redirecting to login...';
                setTimeout(() => this.$router.push('/login'), 1200);
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }
    }
};
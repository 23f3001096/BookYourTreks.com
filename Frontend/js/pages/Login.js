const Login = {
    template: `
        <div class="d-flex justify-content-center align-items-center hero-section" style="min-height: 100vh;">
            <div class="card p-4 shadow" style="width: 380px;">
                <h4 class="mb-3 text-center text-brand"><i class="bi bi-tree-fill"></i> Login</h4>
                <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" required />
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" required />
                    </div>
                    <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                        {{ loading ? 'Logging in...' : 'Login' }}
                    </button>
                </form>
                <p class="text-center mt-3 mb-0">
                    New here? <router-link to="/register">Register</router-link>
                </p>
                <p class="text-center mt-1 mb-0">
                    <router-link to="/">Back to home</router-link>
                </p>
            </div>
        </div>
    `,
    data() {
        return { email: '', password: '', error: '', loading: false };
    },
    methods: {
        async handleLogin() {
            this.error = '';
            this.loading = true;
            try {
                const res = await api.login({ email: this.email, password: this.password });
                const role = res.data.role;
                if (role === 'admin') this.$router.push('/admin/dashboard');
                else if (role === 'staff') this.$router.push('/staff/dashboard');
                else this.$router.push('/customer/dashboard');
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }
    }
};
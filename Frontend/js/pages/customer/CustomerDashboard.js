const CustomerDashboard = {
    template: `
        <div>
            <div class="mb-4">
                <h3 class="text-brand mb-1">Welcome back, {{ userName }}!</h3>
                <p class="text-muted">Here's what's happening with your treks</p>
            </div>

            <loading-spinner v-if="loading"></loading-spinner>
            <div v-else class="row g-3 mb-4">
                <div class="col-md-6">
                    <stat-card label="Available Treks" :value="stats.available_treks" icon="bi bi-map" color="#0f766e"></stat-card>
                </div>
                <div class="col-md-6">
                    <stat-card label="My Active Bookings" :value="stats.my_active_bookings" icon="bi bi-journal-check" color="#2563eb"></stat-card>
                </div>
            </div>

            <div class="row g-3">
                <div class="col-md-4">
                    <router-link to="/customer/treks" class="text-decoration-none">
                        <div class="card p-4 text-center h-100">
                            <i class="bi bi-map text-brand" style="font-size:28px"></i>
                            <p class="mt-2 mb-0 fw-semibold text-dark">Browse Treks</p>
                            <small class="text-muted">Find your next adventure</small>
                        </div>
                    </router-link>
                </div>
                <div class="col-md-4">
                    <router-link to="/customer/bookings" class="text-decoration-none">
                        <div class="card p-4 text-center h-100">
                            <i class="bi bi-journal-check text-brand" style="font-size:28px"></i>
                            <p class="mt-2 mb-0 fw-semibold text-dark">My Bookings</p>
                            <small class="text-muted">View and manage bookings</small>
                        </div>
                    </router-link>
                </div>
                <div class="col-md-4">
                    <router-link to="/customer/history" class="text-decoration-none">
                        <div class="card p-4 text-center h-100">
                            <i class="bi bi-clock-history text-brand" style="font-size:28px"></i>
                            <p class="mt-2 mb-0 fw-semibold text-dark">Trekking History</p>
                            <small class="text-muted">Past treks and export data</small>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    `,
    data() {
        return { stats: {}, userName: '', loading: true };
    },
    async mounted() {
        const meRes = await api.me();
        this.userName = meRes.data.name;
        const res = await api.customerDashboard();
        this.stats = res.data;
        this.loading = false;
    }
};
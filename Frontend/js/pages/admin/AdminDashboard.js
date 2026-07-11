const AdminDashboard = {
    template: `
        <div>
            <div class="mb-4">
                <h3 class="text-brand mb-1">Admin Dashboard</h3>
                <p class="text-muted">Overview of your trekking platform</p>
            </div>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <loading-spinner v-if="loading"></loading-spinner>

            <div v-else>
                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">Overview</h6>
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <stat-card label="Total Treks" :value="dashboard.total_treks" icon="bi bi-map" color="#0f766e"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Users" :value="dashboard.total_users" icon="bi bi-people" color="#2563eb"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Staff" :value="dashboard.total_staff" icon="bi bi-person-badge" color="#0f766e"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Bookings" :value="dashboard.total_bookings" icon="bi bi-journal-check" color="#2563eb"></stat-card>
                    </div>
                </div>

                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">Trek Status Breakdown</h6>
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <stat-card label="Open Treks" :value="stats.open_treks" icon="bi bi-unlock" color="#16a34a"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Completed Treks" :value="stats.completed_treks" icon="bi bi-check-circle" color="#2563eb"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Cancelled Bookings" :value="stats.cancelled_bookings" icon="bi bi-x-circle" color="#dc2626"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Pending/Other" :value="pendingTreks" icon="bi bi-hourglass-split" color="#d97706"></stat-card>
                    </div>
                </div>

                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">Recent Bookings</h6>
                <table class="table table-hover bg-white rounded shadow-sm align-middle mb-4">
                    <thead><tr><th>Trek</th><th>User ID</th><th>Status</th><th>Date</th></tr></thead>
                    <tbody>
                        <tr v-for="b in recentBookings" :key="b.id">
                            <td>{{ b.trek_name }}</td>
                            <td>{{ b.user_id }}</td>
                            <td><status-badge :status="b.status"></status-badge></td>
                            <td>{{ b.booking_date }}</td>
                        </tr>
                        <tr v-if="recentBookings.length === 0"><td colspan="4" class="text-center text-muted py-3">No bookings yet</td></tr>
                    </tbody>
                </table>
                <div class="text-end mb-4">
                    <router-link to="/admin/bookings">View all bookings &rarr;</router-link>
                </div>

                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">Quick Actions</h6>
                <div class="row g-3">
                    <div class="col-md-4">
                        <router-link to="/admin/treks" class="text-decoration-none">
                            <div class="card p-4 text-center h-100">
                                <i class="bi bi-map text-brand" style="font-size:28px"></i>
                                <p class="mt-2 mb-0 fw-semibold text-dark">Manage Treks</p>
                                <small class="text-muted">Create, edit, and monitor treks</small>
                            </div>
                        </router-link>
                    </div>
                    <div class="col-md-4">
                        <router-link to="/admin/staff" class="text-decoration-none">
                            <div class="card p-4 text-center h-100">
                                <i class="bi bi-person-badge text-brand" style="font-size:28px"></i>
                                <p class="mt-2 mb-0 fw-semibold text-dark">Manage Staff</p>
                                <small class="text-muted">Add staff and assign treks</small>
                            </div>
                        </router-link>
                    </div>
                    <div class="col-md-4">
                        <router-link to="/admin/users" class="text-decoration-none">
                            <div class="card p-4 text-center h-100">
                                <i class="bi bi-people text-brand" style="font-size:28px"></i>
                                <p class="mt-2 mb-0 fw-semibold text-dark">Manage Users</p>
                                <small class="text-muted">View and moderate trekkers</small>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return { dashboard: {}, stats: {}, recentBookings: [], loading: true, error: '' };
    },
    computed: {
        pendingTreks() {
            const total = this.dashboard.total_treks || 0;
            const open = this.stats.open_treks || 0;
            const completed = this.stats.completed_treks || 0;
            return Math.max(total - open - completed, 0);
        }
    },
    async mounted() {
        this.loading = true;
        try {
            const [dashRes, statsRes, bookingsRes] = await Promise.all([
                api.adminDashboard(),
                api.adminStats(),
                api.allBookings()
            ]);
            this.dashboard = dashRes.data;
            this.stats = statsRes.data;
            this.recentBookings = bookingsRes.data.slice(0, 5);   // sirf latest 5 dikha
        } catch (err) {
            this.error = err.message;
        } finally {
            this.loading = false;
        }
    }
};
const StaffDashboard = {
    template: `
        <div>
            <div class="mb-4">
                <h3 class="text-brand mb-1">My Dashboard</h3>
                <p class="text-muted">Overview of your assigned treks</p>
            </div>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <loading-spinner v-if="loading"></loading-spinner>

            <div v-else>
                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">Overview</h6>
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <stat-card label="Assigned Treks" :value="treks.length" icon="bi bi-map" color="#0f766e"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Participants" :value="totalParticipants" icon="bi bi-people" color="#2563eb"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Open Treks" :value="openCount" icon="bi bi-unlock" color="#16a34a"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Completed Treks" :value="completedCount" icon="bi bi-check-circle" color="#64748b"></stat-card>
                    </div>
                </div>

                <h6 class="text-muted text-uppercase mb-3" style="font-size:12px;letter-spacing:1px">My Assigned Treks</h6>
                <div v-if="treks.length === 0" class="text-center text-muted py-5">
                    No treks assigned to you yet. Contact your admin.
                </div>
                <div v-else class="row g-3">
                    <div class="col-md-4" v-for="trek in treks" :key="trek.id">
                        <router-link :to="'/staff/treks/' + trek.id" class="text-decoration-none text-dark">
                            <div class="card p-3 h-100">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h5 class="mb-0">{{ trek.name }}</h5>
                                    <status-badge :status="trek.status"></status-badge>
                                </div>
                                <p class="text-muted mb-1"><i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
                                <p class="text-muted mb-2" style="font-size:13px">{{ trek.start_date }} to {{ trek.end_date }}</p>
                                <div class="d-flex justify-content-between" style="font-size:13px">
                                    <span>Slots left: <b>{{ trek.available_slots }}</b></span>
                                    <span>Registered: <b>{{ trek.registered_users }}</b></span>
                                </div>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return { treks: [], loading: true, error: '' };
    },
    computed: {
        totalParticipants() {
            return this.treks.reduce((sum, t) => sum + (t.registered_users || 0), 0);
        },
        openCount() {
            return this.treks.filter(t => t.status === 'open').length;
        },
        completedCount() {
            return this.treks.filter(t => t.status === 'completed').length;
        }
    },
    async mounted() {
        this.loading = true;
        try {
            const res = await api.assignedTreks();
            this.treks = res.data;
        } catch (err) {
            this.error = err.message;
        } finally {
            this.loading = false;
        }
    }
};
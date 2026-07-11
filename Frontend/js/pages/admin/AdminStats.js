const AdminStats = {
    template: `
        <div>
            <h3 class="text-brand mb-1">Reports & Statistics</h3>
            <p class="text-muted mb-4">Platform activity overview</p>

            <loading-spinner v-if="loading"></loading-spinner>

            <div v-else>
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <stat-card label="Total Treks" :value="stats.total_treks" icon="bi bi-map" color="#0f766e"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Open Treks" :value="stats.open_treks" icon="bi bi-unlock" color="#16a34a"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Completed Treks" :value="stats.completed_treks" icon="bi bi-check-circle" color="#2563eb"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Bookings" :value="stats.total_bookings" icon="bi bi-journal-check" color="#0f766e"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Cancelled Bookings" :value="stats.cancelled_bookings" icon="bi bi-x-circle" color="#dc2626"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Customers" :value="stats.total_customers" icon="bi bi-people" color="#2563eb"></stat-card>
                    </div>
                    <div class="col-md-3">
                        <stat-card label="Total Staff" :value="stats.total_staff" icon="bi bi-person-badge" color="#0f766e"></stat-card>
                    </div>
                </div>

                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="card p-4">
                            <h6 class="text-muted mb-3">Trek Status Breakdown</h6>
                            <canvas ref="trekChart" height="220"></canvas>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card p-4">
                            <h6 class="text-muted mb-3">Bookings Overview</h6>
                            <canvas ref="bookingChart" height="220"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return { stats: {}, loading: true, trekChartInstance: null, bookingChartInstance: null };
    },
    async mounted() {
        const res = await api.adminStats();
        this.stats = res.data;
        this.loading = false;

        // DOM update hone ka wait karo, phir chart banao
        this.$nextTick(() => {
            this.renderCharts();
        });
    },
    methods: {
        renderCharts() {
            const trekCtx = this.$refs.trekChart;
            this.trekChartInstance = new Chart(trekCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Open', 'Completed', 'Other'],
                    datasets: [{
                        data: [
                            this.stats.open_treks,
                            this.stats.completed_treks,
                            this.stats.total_treks - this.stats.open_treks - this.stats.completed_treks
                        ],
                        backgroundColor: ['#16a34a', '#2563eb', '#94a3b8'],
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
            });

            const bookingCtx = this.$refs.bookingChart;
            this.bookingChartInstance = new Chart(bookingCtx, {
                type: 'bar',
                data: {
                    labels: ['Total Bookings', 'Cancelled'],
                    datasets: [{
                        label: 'Count',
                        data: [this.stats.total_bookings, this.stats.cancelled_bookings],
                        backgroundColor: ['#0f766e', '#dc2626'],
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });
        }
    },
    beforeUnmount() {
        // page se hatte waqt charts destroy kar, warna memory leak + duplicate chart error aata hai
        if (this.trekChartInstance) this.trekChartInstance.destroy();
        if (this.bookingChartInstance) this.bookingChartInstance.destroy();
    }
};
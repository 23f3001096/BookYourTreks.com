const History = {
    template: `
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="text-brand mb-0">Trekking History</h3>
                <button class="btn btn-outline-primary" @click="exportCSV" :disabled="exporting">
                    <i class="bi bi-download"></i> {{ exporting ? 'Preparing...' : 'Export CSV' }}
                </button>
            </div>

            <div v-if="exportMessage" class="alert alert-info">{{ exportMessage }}</div>

            <loading-spinner v-if="loading"></loading-spinner>
            <table v-else class="table bg-white rounded shadow-sm">
                <thead><tr><th>Trek Name</th><th>Location</th><th>Status</th><th>Booking Date</th></tr></thead>
                <tbody>
                    <tr v-for="b in bookings" :key="b.id">
                        <td>{{ b.trek_name }}</td>
                        <td>{{ b.trek_location || '-' }}</td>
                        <td><status-badge :status="b.status"></status-badge></td>
                        <td>{{ b.booking_date }}</td>
                    </tr>
                    <tr v-if="bookings.length === 0"><td colspan="4" class="text-center text-muted py-3">No history yet</td></tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return { bookings: [], loading: true, exporting: false, exportMessage: '' };
    },
    async mounted() {
        const res = await api.history();
        this.bookings = res.data;
        this.loading = false;
    },
    methods: {
        async exportCSV() {
            this.exporting = true;
            this.exportMessage = '';
            try {
                const res = await api.exportHistory();
                const jobId = res.data.job_id;
                this.exportMessage = 'Export started, checking status...';
                this.pollStatus(jobId);
            } catch (err) {
                this.exportMessage = 'Export failed: ' + err.message;
                this.exporting = false;
            }
        },
        async pollStatus(jobId) {
            const check = async () => {
                const res = await api.exportStatus(jobId);
                if (res.data.status === 'ready') {
                    this.exportMessage = 'Export ready!';
                    window.location.href = res.data.download_url;
                    this.exporting = false;
                } else if (res.data.status === 'processing') {
                    setTimeout(check, 1500);
                } else {
                    this.exportMessage = 'Export failed';
                    this.exporting = false;
                }
            };
            check();
        }
    }
};
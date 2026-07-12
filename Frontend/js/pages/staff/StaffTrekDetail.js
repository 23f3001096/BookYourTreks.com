const StaffTrekDetail = {
    template: `
        <div>
            <router-link to="/staff/dashboard" class="text-decoration-none">&larr; Back to Dashboard</router-link>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <loading-spinner v-if="loading"></loading-spinner>

            <div v-else>
                <div class="card p-4 mt-3 mb-4">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h3 class="text-brand mb-1">{{ trek.name }}</h3>
                            <p class="text-muted mb-2"><i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
                            <status-badge :status="trek.status"></status-badge>
                        </div>
                        <div class="text-end">
                            <p class="mb-1">{{ trek.duration_days }} days · {{ trek.difficulty }}</p>
                            <p class="mb-0">{{ trek.start_date }} to {{ trek.end_date }}</p>
                        </div>
                    </div>

                    <div v-if="trek.status === 'completed'" class="alert alert-secondary mt-3 mb-0">
                        <i class="bi bi-lock-fill"></i> This trek is completed. Only Admin can make further changes.
                    </div>

                    <hr>

                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Available Slots</label>
                            <div class="input-group">
                                <input v-model.number="slotsInput" type="number" min="0" class="form-control"
                                    :disabled="trek.status === 'completed'" />
                                <button class="btn btn-outline-primary" @click="updateSlots" :disabled="trek.status === 'completed'">
                                    Update
                                </button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Trek Status</label>
                            <div class="input-group">
                                <select v-model="statusInput" class="form-select" :disabled="trek.status === 'completed'">
                                    <option value="approved">Approved</option>
                                    <option value="open">Open</option>
                                    <option value="closed">Closed</option>
                                </select>
                                <button class="btn btn-outline-primary" @click="updateStatus" :disabled="trek.status === 'completed'">
                                    Update
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex gap-2 mt-4">
                        <button class="btn btn-primary" @click="markStarted" :disabled="trek.status === 'completed'">
                            <i class="bi bi-play-fill"></i> Mark as Started
                        </button>
                        <button class="btn btn-success" @click="markCompleted" :disabled="trek.status === 'completed'">
                            <i class="bi bi-check-circle"></i> Mark as Completed
                        </button>
                    </div>
                </div>

                <div class="card p-4">
                    <h5 class="mb-3">Registered Participants ({{ trekkers.length }})</h5>
                    <table v-if="trekkers.length > 0" class="table bg-white">
                        <thead><tr><th>User ID</th><th>Status</th><th>Payment</th><th>Booking Date</th></tr></thead>
                        <tbody>
                            <tr v-for="b in trekkers" :key="b.id">
                                <td>{{ b.user_id }}</td>
                                <td><status-badge :status="b.status"></status-badge></td>
                                <td class="text-capitalize">{{ b.payment_status }}</td>
                                <td>{{ b.booking_date }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <p v-else class="text-muted mb-0">No participants registered yet.</p>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            trek: {}, trekkers: [], loading: true, error: '',
            slotsInput: 0, statusInput: ''
        };
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
        async loadData() {
            this.loading = true;
            this.error = '';
            try {
                const trekId = this.$route.params.id;
                const trekRes = await api.staffViewTrek(trekId);
                this.trek = trekRes.data;
                this.slotsInput = this.trek.available_slots;
                this.statusInput = this.trek.status;

                const trekkersRes = await api.staffViewTrekkers(trekId);
                this.trekkers = trekkersRes.data;
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        async updateSlots() {
            try {
                await api.updateSlots(this.trek.id, this.slotsInput);
                await this.loadData();
                alert('Slots updated successfully');
            } catch (err) {
                alert(err.message);
            }
        },
        async updateStatus() {
            try {
                await api.updateTrekStatusStaff(this.trek.id, this.statusInput);
                await this.loadData();
                alert('Status updated successfully');
            } catch (err) {
                alert(err.message);
            }
        },
        async markStarted() {
            try {
                await api.markTrekStarted(this.trek.id);
                await this.loadData();
            } catch (err) {
                alert(err.message);
            }
        },
        async markCompleted() {
            if (!confirm('Mark this trek as completed? This cannot be undone.')) return;
            try {
                await api.markTrekCompleted(this.trek.id);
                await this.loadData();
            } catch (err) {
                alert(err.message);
            }
        }
    }
};
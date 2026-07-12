const MyBookings = {
    template: `
        <div>
            <h3 class="text-brand mb-3">My Bookings</h3>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <loading-spinner v-if="loading"></loading-spinner>
            <div v-else>
                <div v-if="bookings.length === 0" class="text-center text-muted py-5">
                    You haven't booked any treks yet. <router-link to="/customer/treks">Browse treks</router-link>
                </div>
                <table v-else class="table table-hover bg-white rounded shadow-sm align-middle">
                    <thead><tr><th>Trek</th><th>Status</th><th>Payment</th><th>Booking Date</th><th>Actions</th></tr></thead>
                    <tbody>
                        <tr v-for="b in bookings" :key="b.id">
                            <td>{{ b.trek_name }}</td>
                            <td><status-badge :status="b.status"></status-badge></td>
                            <td class="text-capitalize">{{ b.payment_status }}</td>
                            <td>{{ b.booking_date }}</td>
                            <td>
                                <button v-if="b.status === 'booked'" class="btn btn-sm btn-outline-danger" @click="cancel(b.id)">
                                    Cancel
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `,
    data() { return { bookings: [], loading: true, error: '' }; },
    async mounted() { await this.load(); },
    methods: {
        async load() {
            this.loading = true;
            this.error = '';
            try {
                const res = await api.myBookings();
                this.bookings = res.data;
            } catch (err) {
                this.error = err.message || 'Failed to load bookings';
                console.log(this.error)
            } finally {
                this.loading = false;   // 
            }
        },
        async cancel(id) {
            if (!confirm('Cancel this booking?')) return;
            try {
                await api.cancelBooking(id);
                await this.load();
            } catch (err) {
                alert(err.message);
            }
        }
    }
};
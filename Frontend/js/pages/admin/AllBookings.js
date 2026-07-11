const AllBookings = {
    template: `
        <div>
            <h3 class="text-brand mb-3">All Bookings</h3>
            <loading-spinner v-if="loading"></loading-spinner>
            <table v-else class="table table-hover bg-white rounded shadow-sm align-middle">
                <thead><tr><th>ID</th><th>User ID</th><th>Trek</th><th>Status</th><th>Payment</th><th>Booking Date</th></tr></thead>
                <tbody>
                    <tr v-for="b in bookings" :key="b.id">
                        <td>{{ b.id }}</td>
                        <td>{{ b.user_id }}</td>
                        <td>{{ b.trek_name }}</td>
                        <td><status-badge :status="b.status"></status-badge></td>
                        <td>{{ b.payment_status }}</td>
                        <td>{{ b.booking_date }}</td>
                    </tr>
                    <tr v-if="bookings.length === 0"><td colspan="6" class="text-center text-muted py-3">No bookings yet</td></tr>
                </tbody>
            </table>
        </div>
    `,
    data() { return { bookings: [], loading: true }; },
    async mounted() {
        const res = await api.allBookings();
        this.bookings = res.data;
        this.loading = false;
    }
};
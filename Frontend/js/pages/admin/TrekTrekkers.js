const TrekTrekkers = {
    template: `
        <div>
            <router-link to="/admin/treks" class="text-decoration-none">&larr; Back to Treks</router-link>
            <h3 class="text-brand mt-2 mb-3">Trek Details</h3>

            <ul class="nav nav-tabs mb-3">
                <li class="nav-item">
                    <a class="nav-link" :class="{active: activeTab === 'trekkers'}" href="#" @click.prevent="activeTab = 'trekkers'">
                        Participants
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" :class="{active: activeTab === 'reviews'}" href="#" @click.prevent="activeTab = 'reviews'">
                        Reviews
                    </a>
                </li>
            </ul>

            <loading-spinner v-if="loading"></loading-spinner>

            <div v-else>
                <table v-if="activeTab === 'trekkers'" class="table bg-white rounded shadow-sm">
                    <thead><tr><th>User ID</th><th>Status</th><th>Payment</th><th>Booking Date</th></tr></thead>
                    <tbody>
                        <tr v-for="b in bookings" :key="b.id">
                            <td>{{ b.user_id }}</td>
                            <td><status-badge :status="b.status"></status-badge></td>
                            <td class="text-capitalize">{{ b.payment_status }}</td>
                            <td>{{ b.booking_date }}</td>
                        </tr>
                        <tr v-if="bookings.length === 0"><td colspan="4" class="text-center text-muted py-3">No participants yet</td></tr>
                    </tbody>
                </table>

                <div v-if="activeTab === 'reviews'">
                    <div class="card p-4">
                        <p v-if="reviews.length === 0" class="text-muted mb-0">No reviews yet for this trek</p>
                        <div v-for="r in reviews" :key="r.id" class="border-bottom pb-2 mb-2">
                            <div class="d-flex justify-content-between">
                                <b>{{ r.user_name }}</b>
                                <span>
                                    <i v-for="n in 5" :key="n" class="bi"
                                        :class="n <= r.rating ? 'bi-star-fill text-warning' : 'bi-star'"></i>
                                </span>
                            </div>
                            <p class="mb-0 text-muted">{{ r.comment }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return { bookings: [], reviews: [], loading: true, activeTab: 'trekkers' };
    },
    async mounted() {
        const trekId = this.$route.params.id;
        const bookingsRes = await api.trekTrekkers(trekId);
        this.bookings = bookingsRes.data;

        const reviewsRes = await api.viewReviews(trekId);
        this.reviews = reviewsRes.data.reviews;

        this.loading = false;
    }
};
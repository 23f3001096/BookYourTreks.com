const TrekDetails = {
    template: `
        <div>
            <router-link to="/customer/treks" class="text-decoration-none">&larr; Back to Treks</router-link>

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
                            <p class="mb-1"><b>{{ trek.duration_days }}</b> days</p>
                            <p class="mb-1 text-capitalize">{{ trek.difficulty }}</p>
                            <p class="mb-0">Slots left: <b>{{ trek.available_slots }}</b></p>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-md-4"><b>Start Date:</b> {{ trek.start_date }}</div>
                        <div class="col-md-4"><b>End Date:</b> {{ trek.end_date }}</div>
                        <div class="col-md-4" v-if="trek.average_rating">
                            <b>Rating:</b> {{ trek.average_rating }} <i class="bi bi-star-fill text-warning"></i>
                        </div>
                    </div>
                    <button class="btn btn-primary mt-3" @click="bookTrek"
                        :disabled="trek.available_slots === 0 || trek.status !== 'open'">
                        {{ trek.available_slots === 0 ? 'Fully Booked' : (trek.status !== 'open' ? 'Not Open for Booking' : 'Book This Trek') }}
                    </button>
                </div>

                <div class="card p-4">
                    <h5 class="mb-3">Reviews</h5>

                    <div v-if="reviews.length === 0" class="text-muted mb-3">No reviews yet. Be the first!</div>
                    <div v-else class="mb-3">
                        <div v-for="r in reviews" :key="r.id" class="border-bottom pb-2 mb-2">
                            <div class="d-flex justify-content-between">
                                <b>{{ r.user_name }}</b>
                                <span>
                                    <i v-for="n in 5" :key="n" class="bi"
                                        :class="n <= r.rating ? 'bi-star-fill text-warning' : 'bi-star'"></i>
                                </span>
                            </div>
                            <p class="mb-1 text-muted">{{ r.comment }}</p>
                            <div v-if="r.user_id === currentUserId" class="d-flex gap-2">
                                <button class="btn btn-sm btn-outline-primary" @click="editReview(r)">Edit</button>
                                <button class="btn btn-sm btn-outline-danger" @click="deleteReview(r.id)">Delete</button>
                            </div>
                        </div>
                    </div>

                    <button class="btn btn-outline-primary btn-sm" @click="toggleReviewForm">
                        <i class="bi bi-pencil"></i> {{ editingReviewId ? 'Editing Review' : 'Write a Review' }}
                    </button>

                    <div v-if="showReviewForm" class="mt-3">
                        <label class="form-label">Rating</label>
                        <select v-model.number="reviewForm.rating" class="form-select mb-2" style="max-width:150px">
                            <option v-for="n in 5" :key="n" :value="n">{{ n }} Star{{ n > 1 ? 's' : '' }}</option>
                        </select>
                        <label class="form-label">Comment</label>
                        <textarea v-model="reviewForm.comment" class="form-control mb-2" placeholder="Share your experience..."></textarea>
                        <div v-if="reviewError" class="alert alert-danger py-2">{{ reviewError }}</div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-primary btn-sm" @click="submitReview">
                                {{ editingReviewId ? 'Update Review' : 'Submit Review' }}
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" @click="cancelReviewForm">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            trek: {}, reviews: [], loading: true, currentUserId: null,
            showReviewForm: false, editingReviewId: null,
            reviewForm: { rating: 5, comment: '' }, reviewError: ''
        };
    },
    async mounted() {
        const meRes = await api.me();
        this.currentUserId = meRes.data.id;
        await this.loadData();
    },
    methods: {
        async loadData() {
            this.loading = true;
            const trekId = this.$route.params.id;
            const trekRes = await api.trekDetails(trekId);
            this.trek = trekRes.data;

            const reviewRes = await api.viewReviews(trekId);
            this.reviews = reviewRes.data.reviews;
            this.loading = false;
        },
        async bookTrek() {
            try {
                await api.bookTrek(this.trek.id);
                alert('Trek booked successfully! Check your email for payment confirmation.');
                await this.loadData();
            } catch (err) {
                alert(err.message);
            }
        },
        toggleReviewForm() {
            if (this.editingReviewId) {
                this.cancelReviewForm();
            } else {
                this.showReviewForm = !this.showReviewForm;
            }
        },
        editReview(review) {
            this.editingReviewId = review.id;
            this.reviewForm = { rating: review.rating, comment: review.comment };
            this.showReviewForm = true;
        },
        cancelReviewForm() {
            this.showReviewForm = false;
            this.editingReviewId = null;
            this.reviewForm = { rating: 5, comment: '' };
            this.reviewError = '';
        },
        async deleteReview(reviewId) {
            if (!confirm('Delete your review?')) return;
            try {
                await api.deleteReview(reviewId);
                await this.loadData();
            } catch (err) {
                alert(err.message);
            }
        },
        async submitReview() {
            this.reviewError = '';
            try {
                if (this.editingReviewId) {
                    await api.editReview(this.editingReviewId, this.reviewForm);
                } else {
                    await api.addReview(this.trek.id, this.reviewForm);
                }
                this.cancelReviewForm();
                await this.loadData();
            } catch (err) {
                this.reviewError = err.message;
            }
        }
    }
};
const TrekList = {
    template: `
        <div>
            <h3 class="text-brand mb-3">Browse Treks</h3>

            <div class="card p-3 mb-4">
                <div class="row g-2">
                    <div class="col-md-4">
                        <input v-model="filters.location" class="form-control" placeholder="Location" />
                    </div>
                    <div class="col-md-3">
                        <select v-model="filters.difficulty" class="form-select">
                            <option value="">Any Difficulty</option>
                            <option value="easy">Easy</option>
                            <option value="moderate">Moderate</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <input v-model.number="filters.max_duration" type="number" class="form-control" placeholder="Max Duration (days)" />
                    </div>
                    <div class="col-md-2 d-flex gap-2">
                        <button class="btn btn-primary flex-fill" @click="applyFilters">Search</button>
                    </div>
                </div>
            </div>

            <loading-spinner v-if="loading"></loading-spinner>
            <div v-else>
                <div v-if="treks.length === 0" class="text-center text-muted py-5">
                    No treks found matching your criteria
                </div>
                <div v-else class="row g-3">
                    <div class="col-md-4" v-for="trek in treks" :key="trek.id">
                        <router-link :to="'/customer/treks/' + trek.id" class="text-decoration-none text-dark">
                            <trek-card :trek="trek" @book="bookTrek"></trek-card>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            treks: [], loading: true,
            filters: { location: '', difficulty: '', max_duration: null },
            usingSearch: false
        };
    },
    async mounted() {
        await this.loadTreks();
    },
    methods: {
        async loadTreks() {
            this.loading = true;
            const res = await api.availableTreks();
            this.treks = res.data;
            this.loading = false;
        },
        async applyFilters() {
            this.loading = true;
            const params = new URLSearchParams();
            if (this.filters.location) params.append('location', this.filters.location);
            if (this.filters.difficulty) params.append('difficulty', this.filters.difficulty);
            if (this.filters.max_duration) params.append('max_duration', this.filters.max_duration);

            const res = await api.searchTreks(params.toString());
            this.treks = res.data;
            this.usingSearch = true;
            this.loading = false;
        },
        async bookTrek(id) {
            try {
                await api.bookTrek(id);
                alert('Trek booked successfully! Check your email for payment confirmation.');
                await (this.usingSearch ? this.applyFilters() : this.loadTreks());
            } catch (err) {
                alert(err.message);
            }
        }
    }
};
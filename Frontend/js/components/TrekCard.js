const TrekCard = {
    props: ['trek'],
    emits: ['book'],
    template: `
        <div class="card card-trek h-100">
            <div class="bg-brand bg-opacity-10 d-flex align-items-center justify-content-center" style="height:140px">
                <i class="bi bi-mountain text-brand" style="font-size:40px"></i>
            </div>
            <div class="card-body">
                <h5 class="card-title">{{ trek.name }}</h5>
                <p class="text-muted mb-1"><i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
                <p class="text-muted mb-2">{{ trek.duration_days }} days · {{ trek.difficulty }}</p>
                <status-badge :status="trek.status"></status-badge>
                <p class="mt-2 mb-2" style="font-size:13px">Slots left: {{ trek.available_slots }}</p>
                <button class="btn btn-primary btn-sm w-100" @click.stop.prevent="$emit('book', trek.id)"
                    :disabled="trek.available_slots === 0">
                    {{ trek.available_slots === 0 ? 'Full' : 'Book Now' }}
                </button>
            </div>
        </div>
    `
};
const StatCard = {
    props: ['label', 'value', 'icon', 'color'],
    template: `
        <div class="card stat-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <p class="text-muted mb-1" style="font-size:13px">{{ label }}</p>
                    <h3 class="mb-0">{{ value }}</h3>
                </div>
                <i :class="icon" :style="{ color: color, fontSize: '28px' }"></i>
            </div>
        </div>
    `
};
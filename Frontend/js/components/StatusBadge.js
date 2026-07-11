const StatusBadge = {
    props: ['status'],
    template: `
        <span class="badge rounded-pill" :class="badgeClass">{{ status }}</span>
    `,
    computed: {
        badgeClass() {
            const map = {
                open: 'bg-success',
                closed: 'bg-secondary',
                pending: 'bg-warning text-dark',
                approved: 'bg-info text-dark',
                completed: 'bg-primary',
                booked: 'bg-success',
                cancelled: 'bg-danger',
            };
            return map[this.status] || 'bg-secondary';
        }
    }
};
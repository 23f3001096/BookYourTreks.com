const Sidebar = {
    props: ['items'],
    template: `
        <div class="sidebar p-3">
            <router-link
                v-for="item in items"
                :key="item.path"
                :to="item.path"
                class="nav-link d-flex align-items-center gap-2"
                active-class="active"
            >
                <i :class="item.icon"></i> {{ item.label }}
            </router-link>
        </div>
    `
};
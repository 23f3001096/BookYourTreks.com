const Landing = {
    template: `
        <div>
            <nav class="navbar navbar-brand-custom px-4 py-3">
                <span class="navbar-brand fw-bold text-white fs-4">
                    <i class="bi bi-tree-fill"></i> BookYourTreks
                </span>
                <div class="ms-auto">
                    <router-link to="/login" class="btn btn-light btn-sm me-2">Login</router-link>
                    <router-link to="/register" class="btn btn-outline-light btn-sm">Register</router-link>
                </div>
            </nav>

            <div class="hero-section text-center">
                <h1 class="display-4 fw-bold">Explore the Mountains</h1>
                <p class="lead">Book unforgettable treks with expert guides and trusted staff</p>
                <router-link to="/register" class="btn btn-light btn-lg mt-3">Start Trekking</router-link>
            </div>

            <div class="container py-5">
                <h3 class="text-center mb-4 text-brand">Why Choose Us</h3>
                <div class="row g-4">
                    <div class="col-md-4 text-center">
                        <i class="bi bi-shield-check text-brand" style="font-size:36px"></i>
                        <h5 class="mt-2">Verified Staff</h5>
                        <p class="text-muted">Every trek managed by trained trekking staff</p>
                    </div>
                    <div class="col-md-4 text-center">
                        <i class="bi bi-calendar-check text-brand" style="font-size:36px"></i>
                        <h5 class="mt-2">Easy Booking</h5>
                        <p class="text-muted">Book, track, and manage your treks in one place</p>
                    </div>
                    <div class="col-md-4 text-center">
                        <i class="bi bi-star text-brand" style="font-size:36px"></i>
                        <h5 class="mt-2">Top Rated Treks</h5>
                        <p class="text-muted">Real reviews from real trekkers</p>
                    </div>
                </div>
            </div>
        </div>
    `
};
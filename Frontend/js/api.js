const API_BASE = '/api';

async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        cache: 'no-store',
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(API_BASE + endpoint, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || 'Something went wrong');
    }
    return data;
}

const api = {
    // Auth
    register: (payload) => apiCall('/auth/register', 'POST', payload),
    login: (payload) => apiCall('/auth/login', 'POST', payload),
    logout: () => apiCall('/auth/logout', 'POST'),
    me: () => apiCall('/auth/me'),

    // Customer
    customerDashboard: () => apiCall('/customer/dashboard'),
    customerProfile: () => apiCall('/customer/profile'),
    customerEditProfile: (payload) => apiCall('/customer/profile', 'PUT', payload),
    availableTreks: () => apiCall('/customer/treks'),
    searchTreks: (params) => apiCall(`/customer/treks/search?${params}`),
    trekDetails: (id) => apiCall(`/customer/treks/${id}`),
    myBookings: () => apiCall('/customer/bookings'),
    bookTrek: (trekId) => apiCall('/customer/bookings', 'POST', { trek_id: trekId }),
    cancelBooking: (id) => apiCall(`/customer/bookings/${id}/cancel`, 'POST'),
    history: () => apiCall('/customer/bookings'),
    exportHistory: () => apiCall('/customer/history/export', 'POST'),
    exportStatus: (jobId) => apiCall(`/customer/history/export/${jobId}`),

    // Reviews
    viewReviews: (trekId) => apiCall(`/reviews/treks/${trekId}/reviews`),
    addReview: (trekId, payload) => apiCall(`/reviews/treks/${trekId}/reviews`, 'POST', payload),
    editReview: (reviewId, payload) => apiCall(`/reviews/reviews/${reviewId}`, 'PUT', payload),
    deleteReview: (reviewId) => apiCall(`/reviews/reviews/${reviewId}`, 'DELETE'),

    // ---------- Staff ----------
    staffDashboard: () => apiCall('/staff/dashboard'),
    staffProfile: () => apiCall('/staff/profile'),
    staffEditProfile: (payload) => apiCall('/staff/profile', 'PUT', payload),
    assignedTreks: () => apiCall('/staff/treks'),
    staffViewTrek: (id) => apiCall(`/staff/treks/${id}`),
    updateSlots: (id, slots) => apiCall(`/staff/treks/${id}/slots`, 'PUT', { available_slots: slots }),
    updateTrekStatusStaff: (id, status) => apiCall(`/staff/treks/${id}/status`, 'PUT', { status }),
    staffViewTrekkers: (id) => apiCall(`/staff/treks/${id}/trekkers`),
    markTrekStarted: (id) => apiCall(`/staff/treks/${id}/start`, 'POST'),
    markTrekCompleted: (id) => apiCall(`/staff/treks/${id}/complete`, 'POST'),

    // Admin
    adminDashboard: () => apiCall('/admin/dashboard'),
    adminStats: () => apiCall('/admin/stats'),
    adminProfile: () => apiCall('/admin/profile'),
    adminEditProfile: (payload) => apiCall('/admin/profile', 'PUT', payload),
    listTreks: () => apiCall('/admin/treks'),
    viewTrek: (id) => apiCall(`/admin/treks/${id}`),
    createTrek: (payload) => apiCall('/admin/treks', 'POST', payload),
    editTrek: (id, payload) => apiCall(`/admin/treks/${id}`, 'PUT', payload),
    deleteTrek: (id) => apiCall(`/admin/treks/${id}`, 'DELETE'),
    updateTrekStatus: (id, status) => apiCall(`/admin/treks/${id}/status`, 'PATCH', { status }),
    adminSearchTreks: (q) => apiCall(`/admin/treks/search?q=${encodeURIComponent(q)}`),
    trekTrekkers: (id) => apiCall(`/admin/treks/${id}/trekkers`),
    listStaff: () => apiCall('/admin/staff'),
    viewStaff: (id) => apiCall(`/admin/staff/${id}`),
    addStaff: (payload) => apiCall('/admin/staff', 'POST', payload),
    removeStaff: (id) => apiCall(`/admin/staff/${id}`, 'DELETE'),
    assignStaffToTrek: (staffId, trekId) => apiCall(`/admin/staff/${staffId}/assign-trek`, 'POST', { trek_id: trekId }),
    blockStaff: (id) => apiCall(`/admin/staff/${id}/blocklist`, 'POST'),
    activateStaff: (id) => apiCall(`/admin/staff/${id}/activate`, 'POST'),
    searchStaff: (q) => apiCall(`/admin/staff/search?q=${encodeURIComponent(q)}`),
    listUsers: () => apiCall('/admin/users'),
    viewUser: (id) => apiCall(`/admin/users/${id}`),
    blockUser: (id) => apiCall(`/admin/users/${id}/blocklist`, 'POST'),
    activateUser: (id) => apiCall(`/admin/users/${id}/activate`, 'POST'),
    searchUsers: (q) => apiCall(`/admin/users/search?q=${encodeURIComponent(q)}`),
    allBookings: () => apiCall('/admin/bookings'),
};
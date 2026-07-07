# admin_blueprint.py

from blueprints import admin_bp
from flask_login import login_required, current_user

# Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    pass

# Profile
@admin_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    pass

@admin_bp.route('/profile', methods=['PUT'])
@login_required
def edit_profile():
    pass

# Staff related APIs
@admin_bp.route('/staff', methods=['GET'])
@login_required
def list_staff():
    pass

@admin_bp.route('/staff/<int:staff_id>', methods=['GET'])
@login_required
def view_staff_details(staff_id):
    pass

@admin_bp.route('/staff', methods=['POST'])
@login_required
def add_staff():
    pass

@admin_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
@login_required
def remove_staff():
    pass

@admin_bp.route('/staff/<int:staff_id>/assign-trek', methods=['POST'])
@login_required
def assign_staff_to_trek(staff_id):
    pass

# Users related APIs
@admin_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    pass

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def view_user_details(user_id):
    pass

# Blocklist and active related APIs
@admin_bp.route('/users/<int:user_id>/blocklist', methods=['POST'])
@login_required
def blocklist_user(user_id):
    pass

@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@login_required
def active_user(user_id):
    pass

@admin_bp.route('/staff/<int:staff_id>/blocklist', methods=['POST'])
@login_required
def blocklist_staff(staff_id):
    pass

@admin_bp.route('/staff/<int:staff_id>/activate', methods=['POST'])
@login_required
def activate_staff(staff_id):
    pass

# Search related APIs
@admin_bp.route('/staff/search', methods=['GET'])
@login_required
def search_staff():
    pass

@admin_bp.route('/users/search', methods=['GET'])
@login_required
def search_trekkers():
    pass

# Trek APIs
@admin_bp.route('/treks', methods=['GET'])
@login_required
def list_treks():
    pass

@admin_bp.route('/treks', methods=['POST'])
@login_required
def create_trek():
    pass

@admin_bp.route('/treks/<int:trek_id>', methods=['GET'])
@login_required
def view_trek(trek_id):
    pass

@admin_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@login_required
def edit_trek(trek_id):
    pass

@admin_bp.route('/treks/<int:trek_id>', methods=['DELETE'])
@login_required
def delete_trek(trek_id):
    pass

@admin_bp.route('/treks/<int:trek_id>/status', methods=['PATCH'])
@login_required
def update_trek_status(trek_id):
    pass

@admin_bp.route('/treks/search', methods=['GET'])
@login_required
def search_trek():
    pass

@admin_bp.route('/treks/<int:trek_id>/trekkers', methods=['GET'])
@login_required
def trekkers(trek_id):
    pass

# Bookings
@admin_bp.route('/bookings', methods=['GET'])
@login_required
def bookings():
    pass

# Stats / Reports
@admin_bp.route('/stats', methods=['GET'])
@login_required
def stats():
    pass
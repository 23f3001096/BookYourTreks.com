# customer_blueprint.py

from blueprints import customer_bp
from flask_login import login_required, current_user

@customer_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    pass

@customer_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    pass

@customer_bp.route('/profile', methods=['PUT'])
@login_required
def edit_profile():
    pass

@customer_bp.route('/treks', methods=['GET'])
@login_required
def available_treks():
    pass

@customer_bp.route('/treks/search', methods=['GET'])
@login_required
def search_treks():
    pass

@customer_bp.route('/treks/<int:trek_id>', methods=['GET'])
@login_required
def trek_details(trek_id):
    pass

@customer_bp.route('/bookings', methods=['GET'])
@login_required
def bookings():
    pass

@customer_bp.route('/bookings', methods=['POST'])
@login_required
def book_trek():
    pass

@customer_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_bookings(booking_id):
    pass

@customer_bp.route('/history', methods=['GET'])
@login_required
def history():
    pass

@customer_bp.route('/history/export', methods=['POST'])
@login_required
def export_history():
    pass

@customer_bp.route('/history/export/<string:job_id>', methods=['GET'])
@login_required
def export_status(job_id):
    pass
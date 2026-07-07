# review_blueprint.py

from blueprints import review_bp
from flask_login import login_required, current_user

@review_bp.route('/treks/<int:trek_id>/reviews', methods=['GET'])
def view_reviews(trek_id):
    pass

@review_bp.route('/treks/<int:trek_id>/reviews', methods=['POST'])
@login_required
def add_review(trek_id):
    pass

@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@login_required
def edit_review(review_id):
    pass

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    pass
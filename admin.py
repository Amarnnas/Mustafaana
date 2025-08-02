from flask import Blueprint, request, jsonify, session
from src.models.user import db, User

admin_bp = Blueprint('admin', __name__)

def require_admin():
    """التحقق من أن المستخدم مسؤول"""
    if 'user_id' not in session:
        return False
    
    user = User.query.get(session['user_id'])
    return user and user.is_admin

@admin_bp.route('/users', methods=['GET'])
def get_users():
    if not require_admin():
        return jsonify({'error': 'غير مسموح لك بالوصول لهذه الصفحة'}), 403
    
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not require_admin():
        return jsonify({'error': 'غير مسموح لك بحذف المستخدمين'}), 403
    
    # منع حذف المستخدم الحالي
    if user_id == session['user_id']:
        return jsonify({'error': 'لا يمكنك حذف حسابك الخاص'}), 400
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'تم حذف المستخدم بنجاح'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'حدث خطأ أثناء حذف المستخدم'}), 500


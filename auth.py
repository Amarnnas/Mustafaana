from flask import Blueprint, request, jsonify, session
from src.models.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        return jsonify({
            'message': 'تم تسجيل الدخول بنجاح',
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'تم تسجيل الخروج بنجاح'}), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({'authenticated': False}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # التحقق من أن المستخدم الحالي مسؤول
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    current_user = User.query.get(session['user_id'])
    if not current_user or not current_user.is_admin:
        return jsonify({'error': 'غير مسموح لك بإضافة مستخدمين جدد'}), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    
    if not username or not password:
        return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
    
    # التحقق من عدم وجود المستخدم مسبقاً
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'اسم المستخدم موجود مسبقاً'}), 400
    
    # إنشاء مستخدم جديد
    new_user = User(username=username, is_admin=is_admin)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'تم إنشاء المستخدم بنجاح',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'حدث خطأ أثناء إنشاء المستخدم'}), 500


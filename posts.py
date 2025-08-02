from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Post
from datetime import datetime

posts_bp = Blueprint('posts', __name__)

def require_auth():
    """التحقق من تسجيل الدخول"""
    if 'user_id' not in session:
        return False
    return True

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    # البحث
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Post.query
    
    if search:
        query = query.filter(Post.title.contains(search) | Post.content.contains(search))
    
    if category:
        query = query.filter(Post.category == category)
    
    posts = query.order_by(Post.publish_date.desc()).all()
    
    return jsonify({
        'posts': [post.to_dict() for post in posts]
    }), 200

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    category = data.get('category', '')
    
    if not title or not content:
        return jsonify({'error': 'العنوان والمحتوى مطلوبان'}), 400
    
    new_post = Post(
        title=title,
        content=content,
        category=category,
        user_id=session['user_id']
    )
    
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            'message': 'تم إنشاء المنشور بنجاح',
            'post': new_post.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'حدث خطأ أثناء إنشاء المنشور'}), 500

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    post = Post.query.get_or_404(post_id)
    return jsonify({'post': post.to_dict()}), 200

@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    post = Post.query.get_or_404(post_id)
    
    # التحقق من أن المستخدم هو صاحب المنشور أو مسؤول
    current_user = User.query.get(session['user_id'])
    if post.user_id != session['user_id'] and not current_user.is_admin:
        return jsonify({'error': 'غير مسموح لك بتعديل هذا المنشور'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'category' in data:
        post.category = data['category']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'تم تحديث المنشور بنجاح',
            'post': post.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'حدث خطأ أثناء تحديث المنشور'}), 500

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    post = Post.query.get_or_404(post_id)
    
    # التحقق من أن المستخدم هو صاحب المنشور أو مسؤول
    current_user = User.query.get(session['user_id'])
    if post.user_id != session['user_id'] and not current_user.is_admin:
        return jsonify({'error': 'غير مسموح لك بحذف هذا المنشور'}), 403
    
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'تم حذف المنشور بنجاح'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'حدث خطأ أثناء حذف المنشور'}), 500

@posts_bp.route('/categories', methods=['GET'])
def get_categories():
    if not require_auth():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    # الحصول على جميع التصنيفات المستخدمة
    categories = db.session.query(Post.category).filter(Post.category.isnot(None)).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return jsonify({'categories': category_list}), 200


from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Post, Comment
from app.utils.decorator import permission_required


@bp.route('/posts/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def create_post():
    '''添加一篇新文章'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body').strip():
        message['body'] = 'Body is required.'
    if 'category_id' not in data:
        message['category_id'] = 'Category is required.'
    if message:
        return bad_request(message)

    post = Post()
    post.from_dict(data)
    post.category_id = data.get('category_id')
    post.author = g.current_user  # 通过 auth.py 中 verify_token() 传递过来的（同一个request中，需要先进行 Token 认证）
    db.session.add(post)
    # 给文章作者的所有粉丝发送新文章通知
    for user in post.author.followers:
        user.add_notification('unread_followeds_posts_count',
                              user.new_followeds_posts())
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


@bp.route('/posts/', methods=['GET'])
def get_posts():
    '''返回文章集合，分页，可以按分类过滤'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    category_id = request.args.get('category_id', type=int)  # 接收分类ID

    query = Post.query.order_by(Post.timestamp.desc())
    if category_id:
        query = query.filter_by(category_id=category_id)  # 根据分类ID过滤

    data = Post.to_collection_dict(query, page, per_page, 'api.get_posts')
    return jsonify(data)



@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    '''返回一篇文章'''
    post = Post.query.get_or_404(id)
    post.views += 1
    db.session.add(post)
    db.session.commit()
    data = post.to_dict()
    # 下一篇文章
    next_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp > post.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_post', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # 上一篇文章
    prev_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp < post.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_post', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)


@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    '''修改一篇文章'''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body').strip():
        message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    '''删除一篇文章'''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    db.session.delete(post)
    # 给文章作者的所有粉丝发送新文章通知(需要自动减1)
    for user in post.author.followers:
        user.add_notification('unread_followeds_posts_count',
                              user.new_followeds_posts())
    db.session.commit()
    return '', 204


###
# 与博客文章资源相关的资源
##
@bp.route('/posts/<int:id>/comments/', methods=['GET'])
def get_post_comments(id):
    '''返回当前文章下面的一级评论'''
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    # 先获取一级评论
    data = Comment.to_collection_dict(
        post.comments.filter(Comment.parent==None).order_by(Comment.timestamp.desc()), page, per_page,
        'api.get_post_comments', id=id)
    # 再添加子孙到一级评论的 descendants 属性上
    for item in data['items']:
        comment = Comment.query.get(item['id'])
        descendants = [child.to_dict() for child in comment.get_descendants()]
        # 按 timestamp 排序一个字典列表
        from operator import itemgetter
        item['descendants'] = sorted(descendants, key=itemgetter('timestamp'))
    return jsonify(data)


###
# 文章被喜欢/收藏 或 被取消喜欢/取消收藏
###
@bp.route('/posts/<int:id>/like', methods=['GET'])
@token_auth.login_required
def like_post(id):
    '''喜欢文章'''
    post = Post.query.get_or_404(id)
    post.liked_by(g.current_user)
    db.session.add(post)
    # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
    db.session.commit()
    # 给文章作者发送新喜欢通知
    post.author.add_notification('unread_posts_likes_count',
                                 post.author.new_posts_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking this post.'
    })


@bp.route('/posts/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
def unlike_post(id):
    '''取消喜欢文章'''
    post = Post.query.get_or_404(id)
    post.unliked_by(g.current_user)
    db.session.add(post)
    # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
    db.session.commit()
    # 给文章作者发送新喜欢通知(需要自动减1)
    post.author.add_notification('unread_posts_likes_count',
                                 post.author.new_posts_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking this post anymore.'
    })


@bp.route('/posts/export-posts/', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def export_posts():
    '''导出当前用户的所有文章，RQ 后台任务'''
    if g.current_user.get_task_in_progress('export_posts'):  # 如果用户已经有同名的后台任务在运行中时
        return bad_request('上一个导出文章的后台任务尚未结束')
    else:
        # 将 app.utils.tasks.export_posts 放入任务队列中
        g.current_user.launch_task('export_posts', '正在导出文章...', kwargs={'user_id': g.current_user.id})
        return jsonify(message='正在运行导出文章后台任务')


###
# 全文搜索
###
@bp.route('/search/', methods=['GET'])
def search():
    '''Elasticsearch全文检索博客文章'''
    q = request.args.get('q')
    if not q:
        return bad_request(message='keyword is required.')

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    total, hits_basequery = Post.search(q, page, per_page)
    # 总页数
    total_pages, div = divmod(total, per_page)
    if div > 0:
        total_pages += 1

    # 不能使用 Post.to_collection_dict()，因为查询结果已经分页过了
    data = {
        'items': [item.to_dict() for item in hits_basequery],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total
        },
        '_links': {
            'self': url_for('api.search', q=q, page=page, per_page=per_page),
            'next': url_for('api.search', q=q, page=page + 1, per_page=per_page) if page < total_pages else None,
            'prev': url_for('api.search', q=q, page=page - 1, per_page=per_page) if page > 1 else None
        }
    }
    return jsonify(data=data, message='Total items: {}, current page: {}'.format(total, page))


@bp.route('/search/post-detail/<int:id>', methods=['GET'])
def get_search_post(id):
    '''从搜索结果列表页跳转到文章详情'''
    q = request.args.get('q')
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if q and page and per_page:  # 说明是从搜索结果页中过来查看文章详情的，所以要高亮关键字
        total, hits_basequery = Post.search(q, page, per_page)
        post = hits_basequery.first()  # 只会有唯一的一篇文章
        data = post.to_dict()  # 会高亮关键字
    else:
        post = Post.query.get_or_404(id)
        data = post.to_dict()  # 不会高亮关键字

    # 下一篇文章
    next_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp > post.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_post', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # 上一篇文章
    prev_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp < post.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_post', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)

@bp.route('/categories/', methods=['GET'])
def get_categories():
    categories_list = [
        {'id': 1, 'name': '科技'},
        {'id': 2, 'name': '生活'},
        {'id': 3, 'name': '游戏'},
        {'id': 4, 'name': '经济'},
        {'id': 5, 'name': '时尚'},
        {'id': 6, 'name': '文化'}
    ]

    return jsonify(categories_list)
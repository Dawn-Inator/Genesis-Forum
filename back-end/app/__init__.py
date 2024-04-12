import logging
from logging.handlers import RotatingFileHandler
import os
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from flask import Flask, request
from app.api import bp as api_bp
from app.api_v2.app import bp as api_v2_bp
from app.extensions import cors, db, migrate, mail, babel


def create_app(config_class=None):
    '''Factory Pattern: Create Flask app.'''
    app = Flask(__name__)

    # Initialization flask app
    configure_app(app, config_class)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    # 不使用 Jinja2，用不到模版过滤器和上下文处理器
    # configure_template_filters(app)
    # configure_context_processors(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_errorhandlers(app)

    return app

def configure_app(app, config_class):
    app.config.from_object(config_class)
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False
    # 整合RQ任务队列
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('genesis-forum', connection=app.redis, default_timeout=3600)  # 设置任务队列中各任务的执行最大超时时间为 1 小时
    # Elasticsearch全文检索
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


def configure_blueprints(app):
    # 注册 blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(api_v2_bp, url_prefix='/api/v2')


def configure_extensions(app):
    '''Configures the extensions.'''
    # Enable CORS
    cors.init_app(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)
    # Init Flask-Mail
    mail.init_app(app)
    # Init Flask-Babel
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        # return 'zh'  # 这样设置的话，所有用户永远显示中文
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def configure_logging(app):
    '''Configure Logging.'''
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/genesis-forum.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask API Startup')


def configure_before_handlers(app):
    '''Configures the before request handlers'''
    pass


def configure_after_handlers(app):
    '''Configures the after request handlers'''
    pass


def configure_errorhandlers(app):
    '''Configures the error handlers'''
    pass

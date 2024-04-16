import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 日志输出到控制台还是日志文件中
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false').lower() in ['true', 'on', '1']

    # 分页设置
    POSTS_PER_PAGE = 10
    USERS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 10
    TASKS_PER_PAGE = 10
    # Redis 用于 RQ 任务队列
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    # Elasticsearch 全文检索
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or '127.0.0.1:9200'
    # Flask-Babel
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    LANGUAGES = ['zh', 'en']

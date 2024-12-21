# 004
# Try to refactor the following code
# 1. Make it readable and testable
# 2. Please check error handling issues, maybe some error hidden or no-need to emit
# 3. We will focus on how you design new functions. It should be scalable and high reusable.
# others
# 1. Assume database client and Redis client already connected, don't worry about it
# 2. There is no 100% correct answer for this question. Just do your best, we will ask you more during the interview
# 3. Do not use any new third party go modules

# import redis

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# class Redis(object):
#     _pool = None

#     def __init__(self):
#         self._pool = redis.ConnectionPool('localhost', 6379)

#     def get_connection(self):
#         return redis.StrictRedis(connection_pool=self._pool)

# class Teacher(db.Model):
#     __tablename__ = 'teacher'

#     id = db.Column(BIGINT(unsigned=True), primary_key=True)
#     name = db.Column(db.Unicode(128))
#     deleted_at = db.Column(db.DateTime())

#     __table_args__ = (
#         {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_unicode_ci'}
#     )

# app = Flask(__name__)
# db = SQLAlchemy(app)

# @api.route('/admin/teachers', methods=['GET'])
# def get_teachers():
#     deleted = request.args.get('deleted')
#     page = request.args.get('page')
#     size = request.args.get('size')

#     cache = Redis().get_connection()
#     cache_key = '{page}-{size}-{deleted}'.format(page=page, size=size, deleted=deleted)
#     result = cache.get(cache_key)

#     if result:
#         return result
#     else:
#         offset = size * (page - 1)

#         if deleted:
#             teachers = Teacher.query.filter(Teacher.deleted_at != None).offset(offset).limit(size).all()
#         else:
#             teachers = Teacher.query.offset(offset).limit(size).all()

#         cache.set(cache_key, json.dumps(teachers))

#         return jsonify(teachers)


####################################################################################################
# Libraries
####################################################################################################
import datetime
from typing import Any, List, Dict

import redis
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from models.teacher import Teacher


####################################################################################################
# Global Variables
####################################################################################################
app = Flask(__name__)
db = SQLAlchemy(app)


####################################################################################################
# Services
# NOTE: Ideally, this should be in another file, but for simplicity, I will include it here.
####################################################################################################
class RedisClient:
    """A simple Redis client to get and set values in Redis."""

    def __init__(self, host='localhost', port=6379):
        self._pool = redis.ConnectionPool(host=host, port=port)
        self._client = redis.StrictRedis(connection_pool=self._pool)

    def get(self, key: str) -> Any:
        try:
            return self._client.get(key)
        except redis.RedisError as e:
            # Log the error
            print(f"Redis error: {e}")
            return None

    def set(self, key: str, value: Any) -> None:
        try:
            self._client.set(key, value)
        except redis.RedisError as e:
            # Log the error
            print(f"Redis error: {e}")


redis_client = RedisClient()


####################################################################################################
# Models
# NOTE: Ideally, this should be in another file, but for simplicity, I will include it here.
####################################################################################################
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Teacher {self.name}>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'deleted_at': self.deleted_at
        }

    @staticmethod
    def get_teachers(page: int, size: int, deleted: bool = False) -> List['Teacher']:
        """Get a list of teachers with pagination.

        Args:
            page (int): The page number.
            size (int): The number of items per page.
            deleted (bool, optional): Whether to include deleted teachers. Defaults to False.

        Returns:
            List['Teacher']: A list of teachers.
        """
        offset = size * (page - 1)
        query = Teacher.query
        if deleted:
            query = query.filter(Teacher.deleted_at != None)
        return query.offset(offset).limit(size).all()

    @staticmethod
    def get_teacher_by_id(teacher_id: int) -> Teacher:
        """Get a teacher by ID.

        Args:
            teacher_id (int): The ID of the teacher.

        Returns:
            Teacher: The teacher with the given ID.
        """
        return Teacher.query.get(teacher_id)

    def delete(self) -> None:
        """Soft delete the teacher.
        """
        self.deleted_at = datetime.datetime.now()
        self.save()

    def save(self) -> None:
        """Save the teacher to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            # Log the error
            print(f"Database error: {e}")

    def update(self, name: str) -> None:
        """Update the teacher's name.
        """
        self.name = name
        self.save()


####################################################################################################
# API Endpoints
# [GET] /admin/teachers
####################################################################################################
@app.route('/admin/teachers', methods=['GET'])
def get_teachers():
    try:
        # Extract query parameters
        page = request.args.get('page', default=1, type=int)
        size = request.args.get('size', default=30, type=int)
        deleted = request.args.get(
            'deleted', default=False, type=lambda v: v.lower() == 'true')

        # Generate a cache key
        cache_key = f"teachers:{page}:{size}:{deleted}"

        # Try to get data from Redis cache
        cached_teachers = redis_client.get(cache_key)
        if cached_teachers:
            return jsonify(cached_teachers)

        # If not in cache, get data from database
        teachers = Teacher.get_teachers(page, size, deleted)
        teachers_dict = [teacher.to_dict() for teacher in teachers]
        redis_client.set(cache_key, teachers_dict)  # Cache the data

        return jsonify(teachers_dict)

    except Exception as e:
        # Log the error
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred'}), 500

#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        """Check if a user is logged in."""
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        return {}, 204  


class Login(Resource):
    def post(self):
        """Log a user in."""
        json = request.get_json()
        user = User.query.filter_by(username=json['username']).first()
        
        if user and user.authenticate(json['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid credentials"}, 401

class Logout(Resource):
    def delete(self):
        """Log a user out."""
        session.clear()  
        return {}, 204  


api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

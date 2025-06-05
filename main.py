from app import app, db

if __name__ == '__main__':
    # Initialize database tables within an application context
    with app.app_context():
        db.create_all()
    app.run(debug=True)

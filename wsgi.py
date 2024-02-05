from app import app

if __name__ == '__main__':
    app.run(debug=True)
else:
    from gunicorn.app.wsgiapp import WSGIApplication
    app = WSGIApplication()
    app.load_wsgiapp = lambda: app
    app.run()

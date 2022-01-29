"""App Entry Point"""
from livereload import Server
import platform
from apartment_comparison import create_app


app = create_app()

if __name__ == '__main__':
    server = Server(app)
    server.watch('static/')
    if platform.system() == 'Darwin':
        # Mac
        server.serve(port=4600, host='0.0.0.0')
        # app.run(host='0.0.0.0', port='4700', debug=True)
    else:
        # Linux Box
        server.serve(port=5100, host='0.0.0.0')
        # app.run(host='0.0.0.0', port='5000', debug=True)

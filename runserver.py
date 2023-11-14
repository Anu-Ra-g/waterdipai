from api import create_app

server = create_app()

if __name__ == "__main__":
    server.run(host="0.0.0.0")
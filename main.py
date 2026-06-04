from app import create_app
#create the application
app = create_app()
#runs the application
if __name__ == '__main__':
    app.run(debug=True)

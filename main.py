from website import create_app

app = create_app()

if __name__ == '__main__':
    # ! EVERYTIME WE MAKE CHANGES THE WEBSITE WILL RELOAD
    app.run(debug=True)

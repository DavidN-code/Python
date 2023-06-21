from flask_app import app
from flask_app.controllers import users_controller
from flask_app.controllers import recipes_controller



if __name__ == "__main__":  # ensure this file is being 
                            #run directly and not from a different module
    app.run(debug=True)  # run the app in debug mode
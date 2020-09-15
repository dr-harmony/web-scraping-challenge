from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find all records of data from the mongo database
    mars_data = mongo.db.scraped.find_one()

    # # fills database incase it is empty (runs only on first run)
    # if mars_data is None:
    #     mars_scrape = {
    #     "news_title": [""],
    #     "news_p": [""],
    #     "featured_image": "",
    #     "mars_specs": "",
    #     "mars_hem_names": ["", "", "", ""],
    #     "mars_hem_links": ["", "", "", ""]
    #     }
        
    #     mongo.db.scraped.update({}, mars_scrape, upsert=True)
    #     mars_data = mongo.db.scraped.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scrape = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.scraped.update({}, mars_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
from webapp import create_app
from webapp.dtf_news import get_dtf_news

app = create_app()
with app.app.context():
    get_dtf_news()
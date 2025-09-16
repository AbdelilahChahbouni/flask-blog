import json
from flaskblog import current_app , db   # import your Flask app factory
from flaskblog.models import  Post



with current_app.app_context():
    # Load JSON file
    with open("posts.json", "r") as f:
        posts_data = json.load(f)

    for item in posts_data:
        post = Post(
            title=item["title"],
            content=item["content"],
            user_id=item["user_id"]
        )
        db.session.add(post)

    db.session.commit()
    print("Posts imported successfully 🚀")

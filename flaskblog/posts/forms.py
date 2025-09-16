from wtforms import StringField , SubmitField ,TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired , Length



class PostForm(FlaskForm):
     title = StringField('Title' , validators=[DataRequired()])
     content = TextAreaField('Content' , validators=[DataRequired()])
     submit = SubmitField('Create')


class CommentForm(FlaskForm):
    content = TextAreaField("Add a comment", validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post Comment")
from wtforms import Form, validators, StringField


class InputForm(Form):
    city = StringField(
        label='City name:',
        validators=[validators.InputRequired()])
    check_in_date = StringField(
        label='Check in date:  (YYYY-MM-DD)',
        validators=[validators.InputRequired()])
    check_out_date = StringField(
        label='Check in date:  (YYYY-MM-DD)',
        validators=[validators.InputRequired()])
    html_path = StringField(
        label='HTML path: (exists path with new file and html suffix)',
        validators=[validators.InputRequired()])
    rapid_api_key = StringField(
        label='Rapid API Key:',
        validators=[validators.InputRequired()])
    bucket_name = StringField(
        label='S3 bucket name:',
        validators=[validators.InputRequired()])
    s3_object_name = StringField(
        label='s3 object name:',
        validators=[validators.InputRequired()])

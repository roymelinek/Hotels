from flask import Flask, request, render_template
from Hotels import management
from model import InputForm


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def activate_app():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = management(
            form.city.data, form.check_in_date.data,
            form.check_out_date.data, form.html_path.data,
            form.rapid_api_key.data, form.bucket_name.data,
            form.s3_object_name.data
        )
    else:
        result = None

    return render_template(
        'view.html', form=form, result=result
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)

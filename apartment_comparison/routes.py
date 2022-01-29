from audioop import add
from flask import render_template, request, url_for
from flask import current_app as app
from apartment_comparison import db
from apartment_comparison.helpers import FEATURE_TYPE_MAP, convert_data_types_from_strings


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:aptid>/', methods=['GET', 'POST'])
def index(aptid=1):
    if request.method == 'POST':
        aptid = request.form.get('id')
        items = request.form
        converted = convert_data_types_from_strings(items, FEATURE_TYPE_MAP)
        db.update_apartment(converted)
        print(converted)

    current_apt = db.get_apartment(aptid)
    current_apt.pop('id')
    name = current_apt.pop('name')
    address = current_apt.pop('address')
    url = current_apt.pop('url')
    notes = current_apt.pop('notes')
    apartments = db.get_all_apartments()
    return render_template(
        'index.html',
        apartments=apartments,
        aptid=aptid,
        current_apt=current_apt,
        name=name,
        address=address,
        url=url,
        notes=notes,
        feature_type_map=FEATURE_TYPE_MAP,
    )

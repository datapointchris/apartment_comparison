from flask import redirect, render_template, request, url_for
from flask import current_app as app
from apartment_comparison import db
from apartment_comparison.helpers import convert_data_types_from_strings


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:aptid>/', methods=['GET', 'POST'])
def index(aptid=1):
    feature_type_map = db.get_feature_types()
    if request.method == 'POST':
        aptid = request.form.get('id')
        items = request.form
        converted = convert_data_types_from_strings(items, feature_type_map)
        db.update_apartment(converted)

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
        feature_type_map=feature_type_map,
    )


@app.route('/add_feature/', methods=['POST'])
def add_feature():
    print('YOU ARE HERE')
    name = request.form.get('name')
    type = request.form.get('type')
    aptid = request.form.get('aptid')
    print(name, type, aptid)
    db.add_feature(name, type)
    return redirect(url_for('index', aptid=aptid))

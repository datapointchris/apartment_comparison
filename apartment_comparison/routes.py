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
        features = request.form
        features = convert_data_types_from_strings(features, feature_type_map)
        db.update_features(features)
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
    name = request.form.get('name')
    type = request.form.get('type')
    aptid = request.form.get('aptid')
    db.add_feature(name, type)
    return redirect(url_for('index', aptid=aptid))


@app.route('/delete_apartment/', methods=['POST'])
def delete_apartment():
    id = request.form.get('id')
    print(request.form)
    db.delete_apartment(id)
    return redirect(url_for('manage'))


@app.route('/update_apartment/', methods=['POST'])
def update_apartment():
    id = request.form.get('id')
    update_info = request.form
    print(update_info)
    db.update_apartment(update_info)
    return redirect(url_for('manage', aptid=id))


@app.route('/manage/', methods=['GET', 'POST'])
@app.route('/manage/<int:aptid>/', methods=['GET', 'POST'])
def manage(aptid=1):
    apartments = db.get_all_apartments()
    apt = db.get_apartment(aptid)
    id = apt.get('id')
    name = apt.get('name')
    address = apt.get('address')
    url = apt.get('url')
    return render_template(
        'manage.html',
        apartments=apartments,
        aptid=aptid,
        id=id,
        name=name,
        address=address,
        url=url,
    )

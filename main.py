import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
        # If the handler receives a POST request (a form submission),
        # then it should attempt to retrieve the name of the donor and
        # the amount of the donation from the form submission.
        # It should retrieve the donor from the database with the
        # indicated name, and create a new donation with the indicated
        # donor and donation amount. Then it should redirect
        # the visitor to the home page.
    if request.method == 'POST':

        #Attempt E: the first line works, second fails on NotNull integrity
        #gift = Donation(value=request.form['value'], donor=request.form['donor'])
        #gift.create()

        # Attempt D:
        #donor = Donation.donor(name=request.form['donor'])
        #gift = Donation(value=request.form['value'], donor=donor)

        # Attempt C:
        #Donation.create(value=request.form['value'], donor=request.form['donor'])

        # Attempt B: This one got the closest, but the save/create part fails
        #donor = session.get(Donation.donor.name == request.form['donor'])
        #Donation(value=request.form['value'], donor=donor).create()

        # Attempt B2: Also really close; can instantiate but not save
        # peewee.IntegrityError: NOT NULL constraint failed: donation.donor_id
        #donor_id = Donation.get(donor == request.form['donor']).donor_id
        name = request.form['name']
        value = request.form['value']
        existingdonor = Donor.select().where(Donor.name == name).get()
        Donation(donor=existingdonor, value = value).save()
        #Donation(value=request.form['value'], donor_id = request.form['donor_id']).save()
        #Donation.update(value=request.form['value'], donor_id=donor_id)\
        #    .where(Donation.donor == request.form['donor'])\
        #    .execute()

        # Attempt A:
        #Donation.create(value=request.form['value']).where(session.get(Donation.donor.name) == request.form['donor'])
        return(redirect(url_for('all')))

    # If the handler receives a GET request, then it should render
    # the template for the donation creation page.
    return render_template('create.jinja2')


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)


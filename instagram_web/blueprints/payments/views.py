from app import gateway
from flask import Blueprint, render_template, request, redirect, url_for, flash

payments_blueprint = Blueprint('payments',
                            __name__,
                            template_folder='templates')

@payments_blueprint.route("/", methods=["GET"])
def new():
    username = request.args.get('username')
    return render_template("pay.html", token=gateway.client_token.generate(), username=username)

@payments_blueprint.route("/pay", methods=["POST"])
def pay():
    username = request.form.get('username')
    pay = gateway.transaction.sale({
        "amount": request.form.get('amount'),
        "payment_method_nonce": request.form['nonce'],
        "options": {
            "submit_for_settlement": True
        }
    })
    if pay:
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('users.show', username=username))
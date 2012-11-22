# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, g, abort)
from flask.ext.mail import Message
from flaskext.babel import gettext as _
from flask.ext.login import (login_required, login_user, current_user,
                            logout_user, confirm_login, fresh_login_required,
                            login_fresh)

from fbone.models import User
from fbone.extensions import db, cache, mail, login_manager
from fbone.forms import (SignupForm, LoginForm, RecoverPasswordForm,
                         ReauthForm, ChangePasswordForm)


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    page = int(request.args.get('page', 1))
    pagination = User.query.paginate(page=page, per_page=10)
    return render_template('index.html', pagination=pagination, current_user=current_user)


@frontend.route('/search')
def search():
    keywords = request.args.get('keywords', '').strip()
    pagination = None
    if keywords:
        page = int(request.args.get('page', 1))
        pagination = User.search(keywords).paginate(page, 1)
    else:
        flash(_('Please input keyword(s)'), 'error')
    return render_template('search.html', pagination=pagination, keywords=keywords)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash(_("Logged in"), 'success')
            return redirect(form.next.data or url_for('user.index'))
        else:
            flash(_('Sorry, invalid login'), 'error')

    return render_template('login.html', form=form)


@frontend.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    form = ReauthForm(next=request.args.get('next'))

    if request.method == 'POST':
        user, authenticated = User.authenticate(current_user.name,
                                    form.password.data)
        if user and authenticated:
            confirm_login()
            current_app.logger.debug('reauth: %s' % session['_fresh'])
            flash(_('Reauthenticated.'), 'success')
            return redirect('/change_password')

        flash(_('Password is wrong.'), 'error')
    return render_template('reauth.html', form=form)


@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Logged out'), 'success')
    return redirect(url_for('frontend.index'))


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        if login_user(user):
            return redirect(form.next.data or url_for('user.index'))

    return render_template('signup.html', form=form)


@frontend.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = None
    if current_user.is_authenticated():
        if not login_fresh():
            return login_manager.needs_refresh()
        user = current_user
    elif 'activation_key' in request.values and 'email' in request.values:
        activation_key = request.values['activation_key']
        email = request.values['email']
        user = User.query.filter_by(activation_key=activation_key) \
                         .filter_by(email=email).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():
        user.password = form.password.data
        user.activation_key = None
        db.session.add(user)
        db.session.commit()

        flash(_("Your password has been changed, please log in again"),
              "success")
        return redirect(url_for("frontend.login"))

    return render_template("change_password.html", form=form)


@frontend.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash(_('Please see your email for instructions on '
                  'how to access your account'), 'success')

            user.activation_key = str(uuid4())
            db.session.add(user)
            db.session.commit()

            body = render_template('emails/reset_password.html', user=user)
            message = Message(subject=_('Recover your password'), body=body,
                              recipients=[user.email])
            mail.send(message)

            return redirect(url_for('frontend.index'))
        else:
            flash(_('Sorry, no user found for that email address'), 'error')

    return render_template('reset_password.html', form=form)


@frontend.route('/about')
def about():
    return render_template('footers/about.html', active="about")


@frontend.route('/blog')
def blog():
    return render_template('footers/blog.html', active="blog")


@frontend.route('/help')
def help():
    return render_template('footers/help.html', active="help")


@frontend.route('/privacy')
def privacy():
    return render_template('footers/privacy.html', active="privacy")


@frontend.route('/terms')
def terms():
    return render_template('footers/terms.html', active="terms")

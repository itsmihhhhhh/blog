from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db, admin
import json
from .models import User, bcrypt, Blog, Category

from .forms import LoginForm, RegisterForm, BlogForm, PasswordForm


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(Category, db.session))


@app.route("/")
def getAllBlogs():
    blog = Blog.query.order_by(Blog.date.desc()).all()
    user = User.query.all()
    return render_template('home.html',
                           title='Discover',
                           blog=blog,
                           user=user)




@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user=User.query.filter_by(name=form.username.data).first()
        if existing_user is None:
            user = User(name=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            flash('Username already exist')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, request.form['password']
            ):
                login_user(user)
                flash('You can start blogging now, time to shine!')
                return redirect(url_for('personal_page', id=user.id))

            else:
                flash('Invalid username or password.')
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Thanks for using the platform, hope you like it!')
    return redirect('/')


@app.route('/personal_page', methods=['GET'])
@login_required
def personal_page():
    blog = current_user.followed_posts()
    user = User.query.all()
    return render_template('index.html', blog=blog, user=user)

@app.route('/create_blog', methods=['GET','POST'])
@login_required
def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        t = Blog(title=form.title.data,body=form.body.data, author=current_user.get_id())
        db.session.add(t)
        db.session.commit()
        return redirect('/')

    return render_template('create_blog.html',
                           title='Write blog',
                           form=form)

@app.route('/edit_blog/<id>', methods=['GET','POST'])
@login_required
def edit_blog(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    form = BlogForm(formdata=request.form, obj=blog)

    if form.validate_on_submit():
        t = blog
        t.title = form.title.data
        t.body = form.body.data
        db.session.commit()
        flash('Edit blog successfully')
        return redirect(url_for('user', id=blog.author))

    return render_template('edit_blog.html',title='Edit blog',form=form)

@app.route('/edit_password/<id>', methods=['GET','POST'])
@login_required
def edit_password(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = PasswordForm(request.form)

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.cur_password.data):
            u = user
            u.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password has changed!')
            return redirect('/login')
        else:
            flash('Your current password is incorrect, try again!')

    return render_template('edit_pw.html',title='Edit password',form=form)


@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('user.html', user=user, blog=user.blog)


@app.route('/delete_blog/<id>', methods=['GET'])
def delete_blog(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Delete blog successfully')
    return redirect(url_for('user', id=blog.author))

@app.route('/follow/<id>')
@login_required
def follow(id):
    user = User.query.filter_by(id=id).first()
    if user == current_user:
        flash('You cannot follow yourself!')
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(user.name))
    return redirect(url_for('user', id=id))

@app.route('/unfollow/<id>')
@login_required
def unfollow(id):
    user = User.query.filter_by(id=id).first()
    if user == current_user:
        flash('You cannot unfollow yourself!')
    current_user.unfollow(user)
    db.session.commit()
    flash('You unfollow {}.'.format(user.name))
    return redirect(url_for('user', id=id))

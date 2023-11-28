import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Helper function to fetch blog posts from JSON file
def get_blog_posts():
    with open('blog_posts.json', 'r') as file:

        blog_posts = json.load(file)
    return blog_posts


# Helper function to update blog posts in JSON file
def update_blog_posts(blog_posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)


@app.route('/')
def index():
    """
    Renders the index.html template with the list of blog posts.
    """
    blog_posts = get_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Adds a new blog post to the JSON file.
    """
    if request.method == 'POST':
        # Code for handling the POST request and adding a new blog post
        blog_posts = get_blog_posts()
        new_post = {
            'id': len(blog_posts) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts.append(new_post)
        update_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Deletes a blog post from the JSON file based on the given post_id.
    """
    blog_posts = get_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            update_blog_posts(blog_posts)
            break
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Updates a blog post in the JSON file based on the given post_id.
    """
    blog_posts = get_blog_posts()
    post = None
    for p in blog_posts:
        if p['id'] == post_id:
            post = p
            break

    if post is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Code for handling the POST request and updating the blog post
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        update_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
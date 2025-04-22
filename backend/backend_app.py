from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Exploring Python", "content": "Diving into the basics of Python and its versatility."},
    {"id": 4, "title": "Learning Flask", "content": "A beginner's guide to building web apps with Flask."},
    {"id": 5, "title": "Understanding REST APIs", "content": "Explaining the core principles behind RESTful APIs."},
    {"id": 6, "title": "Working with JSON", "content": "How to use JSON for data exchange between server and client."},
    {"id": 7, "title": "Frontend vs Backend",
     "content": "Discussing the differences between frontend and backend development."},
    {"id": 8, "title": "Version Control 101", "content": "An introduction to Git and why version control matters."},
    {"id": 9, "title": "Debugging Tips", "content": "Useful strategies to debug your code effectively."},
    {"id": 10, "title": "Deploying Applications",
     "content": "Steps to deploy your application in a production environment."},
    {"id": 11, "title": "Intro to HTML", "content": "Learn the basics of HTML for creating web pages."},
    {"id": 12, "title": "CSS Styling", "content": "A brief guide to styling web pages using CSS."},
    {"id": 13, "title": "JavaScript Essentials", "content": "Key concepts in JavaScript for dynamic web content."},
    {"id": 14, "title": "Building Interactive UIs", "content": "Techniques for making user interfaces engaging."},
    {"id": 15, "title": "Responsive Design", "content": "How to design web pages that look great on any device."},
    {"id": 16, "title": "APIs in Action", "content": "Examples of how APIs drive modern web applications."},
    {"id": 17, "title": "Data Structures",
     "content": "Understanding the fundamentals of data structures in programming."},
    {"id": 18, "title": "Algorithm Basics",
     "content": "An overview of common algorithms used in software development."},
    {"id": 19, "title": "Coding Best Practices", "content": "Tips for writing clean and maintainable code."},
    {"id": 20, "title": "Introduction to Testing", "content": "Why testing is crucial and how to get started with it."},
    {"id": 21, "title": "Debugging Techniques", "content": "Advanced techniques to troubleshoot and fix code issues."},
    {"id": 22, "title": "Learning by Doing", "content": "The importance of practical experience in mastering coding."}
]


def sort_posts(posts, sort_field, direction):
    """
    Sorts the given list of posts based on a field and direction.

    Args:
        posts (list): List of posts (dictionaries).
        sort_field (str): The field by which to sort ('title' or 'content').
        direction (str): 'asc' for ascending, 'desc' for descending.

    Returns:
        list: Sorted list of posts.
    """
    reverse = (direction == 'desc')
    return sorted(posts, key=lambda post: post[sort_field].lower(), reverse=reverse)


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """
    Handles retrieving and creating blog posts.

    GET:
        - Optional Query Parameters:
            - sort: Field to sort by ('title' or 'content').
            - direction: Sort order ('asc' for ascending or 'desc' for descending).
              Defaults to 'asc'.
        - Returns a JSON list of posts, optionally sorted based on provided parameters.
        - Returns a 400 error if invalid sort parameters are provided.

    POST:
        - Expects a JSON object in the request body with:
            - title (required): The title of the new post.
            - content (required): The content of the new post.
        - Automatically generates a unique integer ID for the new post.
        - Returns a 201 status with a "Created" message on success.
        - Returns a 400 error if the title or content is missing.
    """
    if request.method == 'POST':
        if POSTS:
            next_id = max(post['id'] for post in POSTS) + 1
        else:
            next_id = 1

        new_post = request.get_json()

        if not new_post.get('title'):
            return jsonify({"error": "Missing Title"}), 400
        if not new_post.get('content'):
            return jsonify({"error": "Missing Content"}), 400

        new_post['id'] = next_id
        POSTS.append(new_post)
        return jsonify({"message": "Created"}), 201

    else:
        sort_field = request.args.get('sort')
        direction = request.args.get('direction', 'asc').lower()

        if sort_field and sort_field not in ['title', 'content']:
            return jsonify({
                "error": "Invalid sort field. Allowed values are 'title' or 'content'."
            }), 400

        if direction not in ['asc', 'desc']:
            return jsonify({
                "error": "Invalid sort direction. Allowed values are 'asc' or 'desc'."
            }), 400

        if sort_field:
            sorted_posts = sort_posts(POSTS, sort_field, direction)
        else:
            sorted_posts = POSTS

        return jsonify(sorted_posts), 200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Deletes a blog post by its ID.

    URL Parameter:
        - id: The unique integer identifier of the post to delete.

    Returns:
        - A JSON message indicating successful deletion and a 200 status code if
          the post is found and deleted.
        - A JSON message with a 404 status code if no post with the given id exists.
    """
    for post in POSTS:
        if id == post['id']:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id {id} was not found."
    }), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update(id):
    """
    Updates an existing blog post by its ID.

    URL Parameter:
        - id: The unique integer identifier of the post to update.

    Request Body (JSON):
        - title (optional): The new title of the post.
        - content (optional): The new content of the post.

    Returns:
        - The updated post as JSON with a 200 status code if successful.
        - A 400 error if the request body is missing or invalid.
        - A 404 error if no post with the given id exists.
    """
    new_details = request.get_json()
    if not new_details:
        return jsonify({"error": "Invalid or missing JSON data."}), 400

    for post in POSTS:
        if post['id'] == id:
            if new_details.get('title'):
                post['title'] = new_details['title']
            if new_details.get('content'):
                post['content'] = new_details['content']
            return jsonify(post), 200

    return jsonify({"error": f"No post found with id {id}."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search():
    """
    Searches for blog posts based on title and/or content.

    Query Parameters:
        - title (optional): Search term to be matched within post titles.
        - content (optional): Search term to be matched within post content.

    Returns:
        - A JSON list of posts that contain the search term in either the title or content.
        - An empty list with a 200 status code if no matching posts are found.
    """
    title_query = request.args.get('title', "").lower()
    content_query = request.args.get('content', "").lower()

    list_of_posts = []
    for post in POSTS:
        title_matches = title_query and title_query in post['title'].lower()
        content_matches = content_query and content_query in post['content'].lower()
        if title_matches or content_matches:
            list_of_posts.append(post)

    return jsonify(list_of_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
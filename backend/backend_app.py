from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# In-memory storage for posts
POSTS = []


@app.route('/api/posts', methods=['GET'])
def list_posts():
    """
    List all blog posts. Optionally supports sorting by title or content.

    Query parameters:
    - sort: Specifies the field by which posts should be sorted (title or content).
    - direction: Specifies the sort order, either 'asc' for ascending or 'desc' for descending. Default is 'asc'.

    Returns:
    - A JSON response with the list of posts, sorted if applicable.
    """
    sort_by = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    # Validate 'sort' parameter
    if sort_by and sort_by not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    # Validate 'direction' parameter
    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    sorted_posts = POSTS.copy()  # Work on a copy to avoid changing original order

    if sort_by:
        reverse = True if direction == 'desc' else False
        sorted_posts.sort(key=lambda post: post[sort_by].lower(), reverse=reverse)

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.

    Expects a JSON object in the request body with the fields:
    - title: The title of the new post.
    - content: The content of the new post.

    Returns:
    - A JSON response with the newly added post, including its ID.
    """
    data = request.get_json()

    # Check if required fields are missing
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required."}), 400

    # Generate a unique ID for the new post
    post_id = str(uuid.uuid4())

    new_post = {
        "id": post_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.

    Returns:
    - A JSON message confirming the deletion or an error message if the post was not found.
    """
    post = next((p for p in POSTS if p['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found."}), 404

    POSTS.remove(post)

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post by its ID.

    Expects a JSON object in the request body with optional fields:
    - title: The new title of the post (optional).
    - content: The new content of the post (optional).

    Returns:
    - A JSON response with the updated post, or an error if the post was not found.
    """
    post = next((p for p in POSTS if p['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found."}), 404

    data = request.get_json()

    # Update fields if provided
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title or content.

    Query parameters:
    - title: Search for posts containing this text in the title.
    - content: Search for posts containing this text in the content.

    Returns:
    - A JSON response with the list of matching posts.
    """
    title = request.args.get('title')
    content = request.args.get('content')

    # Filter posts based on query parameters
    filtered_posts = []

    for post in POSTS:
        if title and title.lower() in post['title'].lower():
            filtered_posts.append(post)
        elif content and content.lower() in post['content'].lower():
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    # Ensure the app runs with UTF-8 encoding to support diverse characters
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5002)

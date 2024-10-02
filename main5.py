import json
from flask import Flask, request, redirect, make_response, jsonify, session,render_template
import secrets
import httpx
from oauthlib.oauth2 import WebApplicationClient
from notion_client import Client as NotionClient
import logging
import os
import datetime
from newsfeed import buildnewsfeed
from videofeed import buildvideofeed, buildvideosummary
from notesgen import generate_mcqs_from_text

app = Flask(__name__)

# Configure Flask's built-in session with a fixed SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_fixed_development_secret_key')  # Use a strong, fixed key in production
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Optionally, set SESSION_COOKIE_SECURE to True in production with HTTPS
# app.config['SESSION_COOKIE_SECURE'] = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Notion OAuth credentials
client_id = "client_id_hehe"
client_secret = "client_secret_hehe"
redirect_uri = "http://localhost:3000/redirect"  # Use 'localhost' as per Notion's requirement

dailyNotes = []
dailyNotesv = []
book_files = ['book1.json']
username="Adi A"
profilepic=""

books = []
json_data=[]

for book_file in book_files:
    with open(book_file, 'r') as f:
        book = json.load(f)
        books.append(book)

class NotionAppClient(WebApplicationClient):
    def __init__(self, client_id, client_secret, **kwargs):
        super().__init__(client_id, **kwargs)
        self.client_secret = client_secret
        self.token_url = "https://api.notion.com/v1/oauth/token"

    def login_link(self, redirect_uri, state):
        base_url = "https://api.notion.com/v1/oauth/authorize"
        return self.prepare_request_uri(base_url, redirect_uri=redirect_uri, state=state)

    def fetch_token(self, code):
        token_request = self.token_url
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # Use HTTP Basic Auth for client credentials
        auth = (self.client_id, self.client_secret)

        # Send form data instead of JSON
        response = httpx.post(token_request, data=body, auth=auth)

        if response.status_code != 200:
            logging.error(f"Token exchange failed: {response.text}")
            raise Exception("Failed to exchange token")

        return response.json()  # Return the parsed token response

# Initialize Notion OAuth client
notion_oauth_client = NotionAppClient(client_id=client_id, client_secret=client_secret)

articles=buildnewsfeed()
videos=buildvideofeed("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Q0EfPzTwtanMVSWuK_QXA")


@app.route("/")
def land():
    return render_template("land.html")

@app.route('/login')
def login():
    # Generate a secure state token
    state = secrets.token_urlsafe(16)

    # Store the state in the session
    session['oauth_state'] = state
    logging.debug(f"Setting session oauth_state: {state}")

    # Create the login URL
    login_url = notion_oauth_client.login_link(redirect_uri, state)

    logging.debug(f"Redirecting to login URL: {login_url}")

    return redirect(login_url)

@app.route('/redirect')
def oauth_redirect():
    logging.debug(f"Cookies received on redirect: {request.cookies}")

    # Log entire session data for debugging
    logging.debug(f"Session data: {dict(session)}")

    # Get the state and code from the request
    returned_state = request.args.get('state')
    code = request.args.get('code')


    # Retrieve the stored state from the session
    stored_state = session.get('oauth_state')
    logging.debug(f"Returned State: {returned_state}")
    logging.debug(f"Stored State: {stored_state}")

    # Check if the state matches to avoid CSRF
    if returned_state != stored_state:
        logging.error(f"State mismatch: expected {stored_state}, got {returned_state}")
        return "State mismatch! Possible CSRF attack detected.", 400

    # Clear the state after successful validation to prevent reuse
    session.pop('oauth_state', None)

    # Proceed to exchange the authorization code for the access token
    try:
        token = notion_oauth_client.fetch_token(code)
        print(token)
        global username, profilepic
        username=token['owner']['user']['name']
        profilepic=token['owner']['user']['avatar_url']
        session['oauth_token'] = token  # Store token in session
        logging.debug(f"Stored oauth_token in session: {token}")

        return redirect("/home")
    except Exception as e:
        logging.error(f"Failed to exchange code: {str(e)}")
        return f"Failed to exchange code: {str(e)}", 400


@app.route("/home")
def home():
    return render_template('home3.html', articles=articles, videos=videos,books=books,username=username,profilepic=profilepic, enumerate=enumerate)

@app.route("/newsfeed")
def newsfeed():
    return render_template('newsfeed.html', articles=articles,enumerate=enumerate)

@app.route("/videofeed")
def videofeed():
    return render_template('videofeed.html', videos=videos,enumerate=enumerate)

@app.route("/library")
def library():
    return render_template('library.html',books=books ,enumerate=enumerate)

@app.route("/tests")
def tests():
    return render_template('tests.html',books=books ,enumerate=enumerate)



@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect('/login'))
    logging.debug("Logged out and cleared session.")
    return resp

@app.route('/session')
def display_session():
    # For debugging purposes only. Remove or secure in production.
    return jsonify(dict(session))


@app.route('/updatenotes', methods=['POST'])
def update_notes():
    index = int(request.args.get('index', -1))
    if 0 <= index < len(articles):
        if articles[index] not in dailyNotes:
            dailyNotes.append(articles[index])
    return jsonify({'status': 'success', 'notes_count': len(dailyNotes)})

# Route for saving videos to notes
@app.route('/updatenotesv', methods=['POST'])
def update_notesv():
    index = int(request.args.get('index', -1))
    if 0 <= index < len(videos):
        if videos[index] not in dailyNotesv:
            dailyNotesv.append(videos[index])
    return jsonify({'status': 'success', 'notes_count': len(dailyNotesv)})

@app.route('/create_pages', methods=['POST'])
def create_page():
    print("ping")
    global dailyNotes, dailyNotesv
    token_data = session.get('oauth_token')
    print(token_data)

    if not token_data:
        return jsonify({"status": "error", "message": "Not logged in"}), 303

    # Use async version of Notion client
    notion = NotionClient(auth=token_data['access_token'])

    datetoday = datetime.datetime.now()
    titleDate = datetoday.strftime("%A") + ", " + datetoday.strftime("%d") + " " + datetoday.strftime(
        "%B") + ", " + datetoday.strftime("%Y")

    choiceControl = 0
    try:
        pages = notion.search(filter={"property": "object", "value": "page"})  # await the search
        for page in pages["results"]:
            if page["properties"]["title"]["title"][0]["plain_text"] == titleDate:
                page_id1 = page["id"]
                choiceControl = 1
            elif page["properties"]["title"]["title"][0]["plain_text"] == "Super Notes":
                page_id1 = page["id"]
        print(page_id1)

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": f"Failed to retrieve pages: {str(e)}"})

    noteBlocks = []

    # Handle dailyNotes (News)
    if dailyNotes:
        for item in dailyNotes:
            titleBlock = {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {"type": "text", "text": {"content": item["title"]}}
                    ]
                }
            }

            summaryBlock = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": item["summary"]}}
                    ]
                }
            }

            noteBlocks.append(titleBlock)
            noteBlocks.append(summaryBlock)

    # Handle dailyNotesv (Videos)
    if dailyNotesv:
        for item in dailyNotesv:
            video_id = item["video_link"].split("=")[1]
            page_blocks = buildvideosummary(video_id)
            noteBlocks.extend(page_blocks)  # Append the video blocks to the existing noteBlocks

    # New page or content structure (combined)
    new_page = {
        "parent": {"type": "page_id", "page_id": page_id1},
        "properties": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": titleDate}
                }
            ]
        },
        "children": noteBlocks
    }

    new_content = {
        "children": noteBlocks,
    }

    # Attempt to create or append content
    try:
        if choiceControl == 0 and (dailyNotes or dailyNotesv):
            response = notion.pages.create(**new_page)
            dailyNotes.clear()
            dailyNotesv.clear()
        elif choiceControl == 1 and (dailyNotes or dailyNotesv):
            notion.blocks.children.append(block_id=page_id1, children=noteBlocks)  # append to existing page
            dailyNotes.clear()
            dailyNotesv.clear()

        return jsonify({"status": "success", "message": "Notes successfully created!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to create notes: {str(e)}"})


@app.route('/books/<book_name>')
def book_page(book_name):
    # Find the book in the list by book_name
    book = next((b for b in books if b['book_name'] == book_name), None)

    if not book:
        return "Book not found", 404

    return render_template('book_page.html', book_name=book_name, chapters=book['chapters'],enumerate=enumerate)


@app.route('/books/<book_name>/<int:chapter_id>')
def chapter_page(book_name, chapter_id):
    # Find the book in the list by book_name
    book = next((b for b in books if b['book_name'] == book_name), None)

    if not book:
        return "Book not found", 404

    # Check if the chapter_id is within the range of available chapters
    if chapter_id < 0 or chapter_id >= len(book['chapters']):
        return "Chapter not found", 404

    chapter = book['chapters'][chapter_id]  # Access chapter by index
    return render_template('chapter_page.html', book_name=book_name, chapter=chapter,enumerate=enumerate)

def get_notion_page_text_by_title(notion,parent_page_id, title):

        # Retrieve the page's content
    page_content = notion.blocks.children.list(parent_page_id)
    text_content = ''

    for block in page_content['results']:
        # Only retrieve paragraph-type blocks
        if block['type'] == 'paragraph':
            text_content += block['paragraph']['text'][0]['plain_text'] + '\n'

    print(page_content)
    return text_content.strip()


@app.route("/dailytest")
def dailyTest():
    token_data = session.get('oauth_token')
    global json_data

    if not token_data or 'access_token' not in token_data:
        return jsonify({"error": "OAuth token not found"}), 401

    try:
        notion = NotionClient(auth=token_data['access_token'])
    except Exception as e:
        return jsonify({"error": f"Notion Client initialization failed: {str(e)}"}), 500

    # Generate the title for today's date
    datetoday = datetime.datetime.now()
    titleDate = datetoday.strftime("%A") + ", " + datetoday.strftime("%d") + " " + datetoday.strftime(
        "%B") + ", " + datetoday.strftime("%Y")

    page_title = titleDate

    # Step 1: Search for the page
    try:
        pages = notion.search(filter={"property": "object", "value": "page"})

        parent_page_id_dt = None
        for page in pages["results"]:
            if "properties" in page and "title" in page["properties"]:
                title_property = page["properties"]["title"]
                if title_property["title"]:
                    # Concatenate all plain_text parts in title
                    page_title_text = ''.join([t['plain_text'] for t in title_property["title"]])
                    if page_title_text.strip() == page_title:
                        parent_page_id_dt = page["id"]
                        break

        if not parent_page_id_dt:
            return jsonify({"error": "No page found with today's date title"}), 404

    except Exception as e:
        return jsonify({"error": f"Error searching for the page: {str(e)}"}), 500

    # Step 2: Retrieve page content and extract text
    try:
        text_content = ""

        # Recursive function to handle nested blocks
        def extract_text(blocks):
            nonlocal text_content
            for block in blocks:
                block_type = block.get('type')
                if not block_type:
                    continue

                if block_type == 'paragraph' and 'rich_text' in block['paragraph']:
                    for part in block['paragraph']['rich_text']:
                        text_content += part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type == 'bulleted_list_item' and 'rich_text' in block['bulleted_list_item']:
                    bullet = "- "  # Bullet point symbol
                    for part in block['bulleted_list_item']['rich_text']:
                        text_content += bullet + part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type == 'numbered_list_item' and 'rich_text' in block['numbered_list_item']:
                    number = "1. "  # Numbered list symbol
                    for part in block['numbered_list_item']['rich_text']:
                        text_content += number + part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type in ['heading_1', 'heading_2', 'heading_3'] and 'rich_text' in block[block_type]:
                    if block_type == 'heading_1':
                        prefix = "# "
                    elif block_type == 'heading_2':
                        prefix = "## "
                    elif block_type == 'heading_3':
                        prefix = "### "

                    for part in block[block_type]['rich_text']:
                        text_content += prefix + part.get('plain_text', '') + "\n"

                elif block_type == 'to_do' and 'rich_text' in block['to_do']:
                    checkbox = "[ ] "  # To-do checkbox symbol
                    for part in block['to_do']['rich_text']:
                        text_content += checkbox + part.get('plain_text', '') + "\n"

                elif block_type == 'toggle' and 'rich_text' in block['toggle']:
                    toggle_text = "▶ "  # Toggle symbol
                    for part in block['toggle']['rich_text']:
                        text_content += toggle_text + part.get('plain_text', '') + "\n"

                # Handle other block types as needed

                # If the block has children, recursively extract their text
                if block.get('has_children'):
                    children = notion.blocks.children.list(block_id=block['id'])
                    extract_text(children['results'])

        # Initial fetch of page content
        page_content = notion.blocks.children.list(block_id=parent_page_id_dt, page_size=100)
        extract_text(page_content['results'])

        # Log the extracted text for debugging
        print("Extracted Text Content:")
        print(text_content)

        if not text_content.strip():
            return jsonify({"error": "No text content found in the page"}), 404

        # Step 3: Send text to Gemini API to generate MCQs
        mcq_json = generate_mcqs_from_text(text_content)
        json_data = json.loads(mcq_json)
        print(json_data)
        print(json_data)
        return render_template('quiz.html', total_questions=len(json_data))

        # Return the generated MCQs
        #return jsonify(mcq_json)

    except Exception as e:
        return jsonify({"error": f"Error retrieving page content: {str(e)}"}), 500

@app.route("/weeklytest")
def weeklyTest():
    token_data = session.get('oauth_token')
    global json_data

    if not token_data or 'access_token' not in token_data:
        return jsonify({"error": "OAuth token not found"}), 401

    try:
        notion = NotionClient(auth=token_data['access_token'])
    except Exception as e:
        return jsonify({"error": f"Notion Client initialization failed: {str(e)}"}), 500

    # Generate date range for the past 7 days
    today = datetime.datetime.now()
    week_dates = [
        (today - datetime.timedelta(days=i)).strftime("%A, %d %B, %Y")
        for i in range(7)
    ]

    # Step 1: Search for the pages
    try:
        pages = notion.search(filter={"property": "object", "value": "page"})

        parent_page_ids_wt = []
        for page in pages["results"]:
            if "properties" in page and "title" in page["properties"]:
                title_property = page["properties"]["title"]
                if title_property["title"]:
                    page_title_text = ''.join([t['plain_text'] for t in title_property["title"]]).strip()
                    if page_title_text in week_dates:
                        parent_page_ids_wt.append(page["id"])

        if not parent_page_ids_wt:
            return jsonify({"error": "No pages found for the past week"}), 404

    except Exception as e:
        return jsonify({"error": f"Error searching for the pages: {str(e)}"}), 500

    # Step 2: Retrieve page content and extract text
    try:
        text_content = ""

        # Recursive function to handle nested blocks
        def extract_text(blocks):
            nonlocal text_content
            for block in blocks:
                block_type = block.get('type')
                if not block_type:
                    continue

                if block_type == 'paragraph' and 'rich_text' in block['paragraph']:
                    for part in block['paragraph']['rich_text']:
                        text_content += part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type == 'bulleted_list_item' and 'rich_text' in block['bulleted_list_item']:
                    bullet = "- "  # Bullet point symbol
                    for part in block['bulleted_list_item']['rich_text']:
                        text_content += bullet + part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type == 'numbered_list_item' and 'rich_text' in block['numbered_list_item']:
                    number = "1. "  # Numbered list symbol
                    for part in block['numbered_list_item']['rich_text']:
                        text_content += number + part.get('plain_text', '') + " "
                    text_content += "\n"

                elif block_type in ['heading_1', 'heading_2', 'heading_3'] and 'rich_text' in block[block_type]:
                    if block_type == 'heading_1':
                        prefix = "# "
                    elif block_type == 'heading_2':
                        prefix = "## "
                    elif block_type == 'heading_3':
                        prefix = "### "

                    for part in block[block_type]['rich_text']:
                        text_content += prefix + part.get('plain_text', '') + "\n"

                elif block_type == 'to_do' and 'rich_text' in block['to_do']:
                    checkbox = "[ ] "  # To-do checkbox symbol
                    for part in block['to_do']['rich_text']:
                        text_content += checkbox + part.get('plain_text', '') + "\n"

                elif block_type == 'toggle' and 'rich_text' in block['toggle']:
                    toggle_text = "▶ "  # Toggle symbol
                    for part in block['toggle']['rich_text']:
                        text_content += toggle_text + part.get('plain_text', '') + "\n"

                # Handle other block types as needed

                # If the block has children, recursively extract their text
                if block.get('has_children'):
                    children = notion.blocks.children.list(block_id=block['id'], page_size=100)
                    extract_text(children['results'])

        # Retrieve content from each page in the past week
        for parent_page_id in parent_page_ids_wt:
            page_content = notion.blocks.children.list(block_id=parent_page_id, page_size=100)
            extract_text(page_content['results'])

        # Log the extracted text for debugging
        print("Extracted Text Content for Weekly Test:")
        print(text_content)

        if not text_content.strip():
            return jsonify({"error": "No text content found in the pages"}), 404

        # Step 3: Send text to Gemini API to generate MCQs
        mcq_response = generate_mcqs_from_text(text_content)

        # Debug: Print the Gemini API response
        print("Response from Gemini API:")
        print(mcq_response)

        # Log the type of mcq_response
        print(f"Type of mcq_response: {type(mcq_response)}")

        # Handle the response based on its type
        if isinstance(mcq_response, str):
            # If it's a JSON string, parse it
            try:
                json_data = json.loads(mcq_response)
                print("Decoded JSON successfully")
            except json.JSONDecodeError as json_err:
                print(f"JSON decoding error: {json_err}")
                print(f"Problematic JSON: {mcq_response}")
                return jsonify({"error": f"JSON decoding failed: {str(json_err)}"}), 500
        elif isinstance(mcq_response, list) or isinstance(mcq_response, dict):
            # If it's already a Python object, use it directly
            json_data = mcq_response
        else:
            # Unexpected format
            return jsonify({"error": "Unexpected response format from Gemini API"}), 500

        # Ensure that json_data is a list
        if not isinstance(json_data, list):
            return jsonify({"error": "MCQ data is not a list"}), 500

        # Return the generated MCQs (you can adjust this as needed)
        return render_template('quiz.html', total_questions=len(json_data))

    except Exception as e:
        return jsonify({"error": f"Error retrieving page content: {str(e)}"}), 500


@app.route('/get_question/<int:question_id>')
def get_question(question_id):
    global json_data
    if 0 <= question_id < len(json_data):
        return jsonify(json_data[question_id])
    else:
        return jsonify({"error": "Invalid question ID"})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global json_data
    data = request.get_json()
    question_id = data['question_id']
    selected_answer = data['selected_answer']

    correct_answer = json_data[question_id]['answer']  # Corrected from `questions` to `quiz_data`

    if selected_answer == correct_answer:
        return jsonify({'is_correct': True})
    else:
        return jsonify({'is_correct': False})





if __name__ == '__main__':
    # Access the app via localhost to match redirect_uri
    app.run(host='localhost', port=3000, debug=True)

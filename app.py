from flask import Flask, jsonify, request
from chatfuel import Chatfuel
from config_logger import custom_logger

app = Flask(__name__)

logger = custom_logger()


@app.route('/')
def hello_world():

	res = {
		"company": "Dimension, Machineria (ITALY) ",
		"facebook_page": "Feel like an artist",
	}
	return jsonify(res)


@app.route('/responsebridge', methods=['POST'])
def response_bridge():

	data = request.get_json()
	chatfuel = Chatfuel()
	answer = chatfuel.handle_answer(data)
	return jsonify(answer)

@app.route('/redirect', methods=['POST'])
def redirect_blocks():

	data = request.get_json()
	if 'block' in data:
		chatfuel = Chatfuel()
		redirect = chatfuel.redirect_block(data)
		return jsonify(redirect)

@app.route('/gallery', methods=['POST'])
def gallery():

	logger.info("Gallery Request")

	data = request.get_json()

	query = ""
	if 'intensity' in data:
		query = data['intensity']

	chatfuel = Chatfuel()
	gallery = chatfuel.galleries(query)
	return gallery

@app.route('/sendimage', methods=['POST'])
def send_images():

	"""
	{
	    "url_image": ""
	}
	"""

	logger.info("Send image")

	data = request.get_json()
	url_image = ""
	if 'url_image' in data:
		url_image = data['url_image']

	chatfuel = Chatfuel()
	image = chatfuel.send_images(url_image)

	return image




if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5022)

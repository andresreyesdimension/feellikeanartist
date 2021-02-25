from config_logger import custom_logger
logger = custom_logger()


class ChatComponents(object):

	def __init__(self):
		self.elements = list()

	def card_gallery(self, title, image_url, sub_title, redirect_block):

		card = {
			"title": title,
			"image_url": image_url,
			"set_attributes": {
				"image": image_url
			},

			"subtitle": sub_title,
			"buttons": [
				{
					"type": "show_block",
					"block_names": [redirect_block],
					"title": "Show me",
					"set_attributes": {"image": image_url}
				}
			]
		}

		self.elements.append(card)

	def gallery_component(self):
		gallery = {
			"messages": [
				{
					"attachment": {
						"type": "template",
						"payload": {
							"template_type": "generic",
							"image_aspect_ratio": "square",
							"elements": self.elements
						}
					}
				}
			]
		}
		return gallery






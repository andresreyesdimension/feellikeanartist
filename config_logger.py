import logging
import logging.config
import os
from datetime import date

def custom_logger():

	today = date.today()

	data = today.strftime("%d%m%Y")

	root_dir = os.path.dirname(os.path.abspath(__file__))  # os.path.join(os.getcwd())
	log_path = os.path.join(root_dir, 'logs', '{}.log').format(data)

	log_format = '%(asctime)s %(name)s %(levelname)s:%(message)s'
	date_format = '%Y-%m-%d %H:%M:%S'
	logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO, datefmt=date_format, filemode = 'w')
	log_obj = logging.getLogger(__name__)
	return log_obj



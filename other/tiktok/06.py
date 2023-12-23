import configparser

config=configparser.ConfigParser()
config.read('config.ini')

print(config['settings']['url'])

config.set('settings','url','20')

with open('config.ini','w') as f:
	config.write(f)
#EDITED

from flask import Flask, jsonify, abort, request, Response, render_template, url_for
from flask_bootstrap import Bootstrap
import rest

app = Flask(__name__)
Bootstrap(app)

switchValue = "ON"



@app.route('/api/v1.0/StartAndStop/<int:click>',methods=['GET'])
def OnOffRoomba(click):
    if(int(click) == 1):
       # rest.send(url="http://192.168.1.6/arduino/start/1")
        print("ON")

    else:
        #rest.send(url="http://192.168.1.6/arduino/start/0")
        print("OFF")

    return "SUCCESS"


@app.route('/api/v1.0/Stars/<float:stars>',methods=['DELETE'])
def manageRating(stars):
    stars=float(stars)
    starsString=str(stars)
    #rest.send(url="http://192.168.1.6/arduino/stars/"+starsString)
    print(starsString)
    return Response(status=200)

@app.route('/api/v1.0/updateArduino/<int:value>',methods=['GET'])
def updateArduino(value):
    if(int(value)==1):
        print("ON")
        switchValue="ON"

    else:
        print("OFF")
        switchValue="OFF"


@app.route('/api/v1.0/updateAndroid',methods=['GET'])
def updateApp():
    return switchValue

@app.route('/api/v1.0/arduinoInput/<int:value>',methods=['GET'])
def arduinoInput(value):
    base_url = 'http://192.168.1.5:8083'
    username = 'admin'
    password = 'amiclean'

    all_devices = rest.send(url=base_url + '/ZWaveAPI/Data/0', auth=(username, password))

    all_devices = all_devices['devices']


    all_devices.pop('1')
    all_devices.pop('3')
    all_devices.pop('9')

    device_url = base_url + '/ZWaveAPI/Run/devices[{}].instances[{}].commandClasses[{}]'
    switch_binary = '37'

    for device_key in all_devices:

        for instance in all_devices[device_key]['instances']:

            if switch_binary in all_devices[device_key]['instances'][instance]['commandClasses']:
                if (int(value) == 1):
                  print('Turning on device %s...' % device_key)
                  url_to_call = (device_url + '.Set(255)').format(device_key, instance, switch_binary)
                  rest.send(url=url_to_call, auth=(username, password))
                else:
                 print('Turning off device %s...' % device_key)

                 url_to_call = (device_url + '.Set(0)').format(device_key, instance, switch_binary)
                 rest.send(url=url_to_call, auth=(username, password))

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060,debug=True)

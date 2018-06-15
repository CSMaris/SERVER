import rest
import time


if __name__ == '__main__':


    base_url = 'http://192.168.1.5:8083'#ip di raspberry

    username = 'admin'
    password = 'amiclean'


    all_devices = rest.send(url=base_url + '/ZWaveAPI/Data/0', auth=(username, password))

    all_devices = all_devices['devices']

    all_devices.pop('1')
    all_devices.pop('3')
    all_devices.pop('4')



    device_url = base_url + '/ZWaveAPI/Run/devices[{}].instances[{}].commandClasses[{}]'



    sensor_binary = '48'
    while(1):

     for device_key in all_devices:
          for instance in all_devices[device_key]['instances']:
              if sensor_binary in all_devices[device_key]['instances'][instance]['commandClasses']:

                  url_to_call = device_url.format(device_key, instance, sensor_binary)

                  response = rest.send(url=url_to_call, auth=(username, password))

                  val = response['data']['1']['level']['value']
                  if(str(val) is 'True'):
                      rest.send(url='http://192.168.1.6/arduino/start/0')



                  print(str(val))


     for i in range(0, 1):
            time.sleep(1)

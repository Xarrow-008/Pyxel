import requests, os
site = 'https://www.nuitducode.net'
url = site + '/storage/depot-jeux/python/nbzm/9ujen'
py = requests.get(url + '/4.pyxres')
with open('4.pyxres', 'wb') as file:
    file.write(py.content)
pyxres = requests.get(url + '/app.py')
with open('app.py', 'wb') as file:
    file.write(pyxres.content)
os.system('pyxel run "4.pyxres"')
# username-availability-checker
A web app by [Gyan Lakhwani](https://github.com/gyanl) and [Manvendra Singh](https://github.com/manu-chroma) to check if a username is taken on Facebook, Twitter, Instagram, Soundcloud & Github.  
Hosted on https://username-check.herokuapp.com/   

##API
API hosted on https://username-availabilty.herokuapp.com/   
How to query API: ```https://username-availabilty.herokuapp.com/check/<website name>.com/<username>/  ```   
eg: https://username-availabilty.herokuapp.com/check/facebook.com/yolo 

##Install Dependencies using Pip
```
pip install -r requirements.txt
```

##Running script in terminal/command prompt
```
python username.py
```

##Running the web app
Both commands must be running for the app to function. Open the address generated when you run flask_backend.py in a browser to use.
```
cd flask
python username_api.py #for launching API
python flask_backend.py #for launching the Website
```

Thanks to [Rohan](https://github.com/rhnvrm) for help with calling the API asynchronously from the html file.

##License
```
© MIT
```

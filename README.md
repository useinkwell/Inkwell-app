"#Inkwell"

# API Documentation

To compile the API Documentation:

- activate the project pip environment
- update the project installations: **pip install -r requirements.txt**  (this should install sphinx, which is needed for this)
- navigate to the "docs" directory: **cd docs**
- with the environment still activated, compile the documentation with the command: **make html** (this compiles all the rst files in the "source" directory and creates a "build" directory).
- in your file explorer, go to the build directory --> html and open index.html   (the project root directory --> docs --> build --> html --> index.html)

The full API documentation can be navigated in the browser from there.

<br/>

# Backend
## Setting up the .env file
A .env file is used to store the SECRET_KEY and CRYPTOGRAPHY_KEY defined in
settings.py. The **SECRET_KEY** can be any string of random characters. A quick and easy way
to generate one consisting of 64 random characters:

**import secrets**<br/>
**key = secrets.token_urlsafe(64)**<br/>

Copy the generated secret key and place in the .env file to look like this:
> SECRET_KEY=VlVtrWj5XKUlynbezqEypeXSGcPklsuzTS2QWlBk3ijPobVZeTRcY5AOdC_M_iH7NAzG1DNiMkvqDbiKkTIowA

The **CRYPTOGRAPHY_KEY** on the other hand must follow a certain rule to be acceptable.
It must consist of 32 url-safe base64-encoded bytes. To generate one, simply do:

**from cryptography.fernet import Fernet**<br/>
**key = Fernet.generate_key()**

The resulting cryptography key is an encoded string of this form:<br/>
> b'ap86bphkL5ArilCtU4SP1aHMNfmPQyys8Tt3lnofEJ8='

Copy only the string part and place in the .env file, to look like this:
> CRYPTOGRAPHY_KEY=ap86bphkL5ArilCtU4SP1aHMNfmPQyys8Tt3lnofEJ8=
    


"#Inkwell"

# API Documentation

To compile the API Documentation:

- activate the project pip environment
- update the project installations: **pip install -r requirements.txt**  (this should install sphinx, which is needed for this)
- navigate to the "docs" directory: **cd docs**
- with the environment still activated, compile the documentation with the command: **make html** (this compiles all the rst files in the "source" directory and creates a "build" directory).
- in your file explorer, go to the build directory --> html and open index.html   (the project root directory --> docs --> build --> html --> index.html)

The full API documentation can be navigated in the browser from there.

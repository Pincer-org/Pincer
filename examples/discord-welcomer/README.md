# Image welcomer

A basic implementation of a welcome message with image. Utilized the xiler html -> img
API.

This script has been build more extensive, which could provide some idea's on how you
can load cogs and structure your project so that it is easily maintainable.

![image](https://user-images.githubusercontent.com/38541241/162048398-b9942760-ea67-4f0d-99cd-ebd05c78fd63.png)

## Setup

1. Install all dependencies with pip from the requirements.txt
   file. _(`pip install -r requirements.txt`)_
2. Copy the `.env.example` file to `.env`, and fill in the expected values.
3. Run the `main.py` file.

## Limitations

This uses the free version of the html->image api. Which restricts to a max of 100
requests per day. _(window sliding)_
You could properly handle this by looking at the HTTP headers, but this example does not
cover that.


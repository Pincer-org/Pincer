# Image welcomer

A basic implementation of a welcome message with image. Utilized the xiler html -> img
API.

This script has been build more extensive, which could provide some idea's on how you
can load cogs and structure your project so that it is easily maintainable.

![image](https://user-images.githubusercontent.com/38541241/162184018-770c8568-4a51-48d8-8f71-e8df68ef62eb.png)

Variant:
![image](https://user-images.githubusercontent.com/38541241/162183991-39a0d3ca-8b77-406f-9c4c-41c213ba3c99.png)

## Setup

1.  Install all dependencies with pip from the requirements.txt
    file. _(`pip install -r requirements.txt`)_

2.  Copy the `.env.example` file to `.env`, and fill in the expected values.

3.  Run the `main.py` file.

## Limitations

This uses the free version of the html->image api. Which restricts to a max of 100
requests per day. _(window sliding)_
You could properly handle this by looking at the HTTP headers, but this example does not
cover that.

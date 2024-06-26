# MemberFinderPro

MemberFinderPro is a web application designed to search and scrape Facebook groups for members' information such as names and contact details.

## Features

- *Login System:* Secure login system with username and password authentication.
- *Facebook Group Scraping:* Scrapes Facebook groups for member information.
- *Data Processing:* Cleans and processes scraped data, including extracting phone numbers.
- *Search Functionality:* Allows users to search for specific information within scraped data.
- *Integration:* Integrates with Elasticsearch for efficient data querying.

## Technologies Used

- *Python:* Backend programming language.
- *Flask:* Web framework for Python.
- *Selenium:* Web automation tool for scraping.
- *Beautiful Soup:* Python library for pulling data out of HTML and XML files.
- *Elasticsearch:* Search engine for data storage and retrieval.
- *Google Cloud Platform:* Deployment platform.

## Installation

1. Clone the repository:

git clone https://github.com/nisabasar/MemberFinderPro.git

2. Install dependencies:

pip install -r requirements.txt

3. Set up environment variables for credentials and configurations.

## Usage

1. Update the login details in the code with your own Facebook username and password.

2. Run the Flask application: python app.py

3. Access the application at [http://localhost:5000](http://localhost:5000).

4. Login with your credentials. (username:admin , password:F.user.41)

5. Enter the Facebook group URL and search keywords (multiple keywords can be entered separated by commas, e.g., "electric, electronic, auto") to start scraping.

6. View search results and download if necessary.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

# instaflex
Instaflex is a social media app that allows a user to interact with other users such as comments, adding a friend, following a person or page, create a posts, etc. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

### Prerequisites

To run this project, you must have the following installed:

- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)

### Installation
1. Install the Python dependencies:

    pip install -r requirements.txt

### Docker Installation 

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/instaflex.git

2. Navigate to the project directory:
    cd instaflex

3. Build the Docker image:
    docker build -t flask-insta-flex .

4. Run the Docker container:
    docker run -p 5000:5000 flask-insta-flex


# RateALeg

## Description

RateALeg is designed to connect theatre-goers from all over Glasgow, letting people know where their favourite shows are being played, while also allowing people to score different aspects of the show such as the soundtrack, cast and set design, as well as leave a review if they wish. 

## Installation Instructions

Please ensure you have Conda and Python installed on your system before proceeding.

1. **Clone the Repository**
```bash
git clone https://github.com/grashop04/RateALeg.git
cd ratealeg
```

2. **Create and Activate a Virtual Environment**
```bash
conda create -n plays python=3.11
conda activate plays
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Populate the Database**
```bash
python populate_plays.py
```

6. **Run the Server**
```bash
python manage.py runserver
```

Visit the 'http://127.0.0.1:8000/' in your web browswer to access the application.

## Contributing

1. Fork this repository.
2. Clone the forked repository onto your local machine.
3. Follow the [Installation Instructions](#installation-instructions).
4. Work on the project locally and test your changes.
5. Commit your changes with a meaningful commit message.
6. Push your changes to your fork.
7. Create a pull request to the original repository.
8. Wait for your pull request to be reviewed and merged.


## Acknowledgements

- Google Maps API for the theatre locations.
- Bootstrap for responsive design and UI components.

## Team 8E Members

- Callum Neilson
- Molly Robertson 
- Diana Polese-Abramowicz
- Ross Simpson
- Zeyu Wang


## Licensing
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



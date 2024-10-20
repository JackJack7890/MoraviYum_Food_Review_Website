# MoraviYum Food Review Website

An online web application designed for Moravian University students to help each other out by sharing their thoughts and opinions on the various foods provided on campus!

Project designed for the Lehigh Valley Collegiate Hackathon 2024.

## Video Demonstration
[MoraviaYum Demo - Lehigh Valley Hackathon 2024](https://youtu.be/-onicEIKR9M)

## Contributers
- [Christine Colvin](https://github.com/christinecolvin)
- [Jack Drabic](https://github.com/JackJack7890)
- [Rafael Garcia Jr.](https://github.com/RGJ-713)
- [Michael Romero](https://github.com/MichaelRomero1)

## How It Works

Moravian students are greeted to a homepage where they can log in with their university email accounts.

![homepage](MoraviYum_home.png)

Once logged in, the user can then select one of two dining locations from the Moravian campus, "The B&G Cafe" or "DeLight's Cafe". They can select these locations and be presented a list of various food vendors from that location.

Once a vendor is selected, they can then select the food they want to leave a review and leave a rating from 1-5.

![reviewpage](MoraviYum_review.png)

## What Was Used
- HTML, CSS, and JavaScript were used for the UI
- A MySQL database is used to store user accounts, food data, and review information
- Images are stored in an S3 bucket
- Google OAUTH is used for ensuring only Moravian students are allowed to sign-in

## Accomplishments
- Laying the foundations and functionality of the vendor/food selection and review
- Successful set-up of the database with working images that correspond to each food item
- Successful implementation of a user login/logout feature through OAUTH

## Future Plans
- A filtering feature to filter foods by rating, prices, calories, etc.
- A "keyword" feature that lets users attribute certain descriptions to certain foods (ex: "PRO: Good price", "CON: Too many calories")


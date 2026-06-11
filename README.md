# CSC426

Coursework repository for CSC426. This is where the practical work for the course is kept across the semester.

The current submission is the weekly dev exercise, which has two separate tasks:

1. A desktop calculator built with Python and Tkinter (myCalculator).
2. A web login authentication app built with HTML, CSS, JavaScript and PHP.

**Live login app:** https://ola.totalh.net/

Each task sits in its own folder and has its own README with more detail.

## Repository structure

```
.
├── calculator/        myCalculator, Python Tkinter desktop app
│   ├── myCalculator.py
│   └── README.md
└── web app/             PHP login authentication app (hosted online)
    ├── index.html
    ├── style.css
    ├── script.js
    ├── login.php
    ├── users.php
    ├── dashboard.php
    ├── logout.php
    └── README.md
```

## 1. myCalculator (Python Tkinter desktop app)

A desktop GUI calculator. The whole expression you type is shown in the display, and the answer is added after you press `=`. For example, typing `2 + 4 - 93` and pressing `=` shows `2+4-93=-87`. It supports addition, subtraction, multiplication, division, integer division, power and modulo, along with Clear and backspace, and it follows normal operator precedence.

This is a desktop application, so it runs on your computer rather than in a browser.

### Requirements

Python 3.8 or newer. Tkinter is included with Python on Windows and macOS. On most Linux setups it ships separately, so if you see a Tkinter error, install it with `sudo apt install python3-tk` on Debian or Ubuntu, or `sudo pacman -S tk` on Arch.

### Run

```bash
cd calculator
python3 myCalculator.py
```

The calculator window will open. More detail is in `calculator/README.md`.

## 2. Login app (hosted online)

A login screen with username and password fields, a login button and a reset button. Input is validated in the browser and again on the server, passwords are stored as bcrypt hashes, and a successful login opens a dashboard page that is protected by a PHP session.

### Where it is and how to reach it

The app is live and hosted here:

**https://ola.totalh.net/**

Open that link in any browser. You will land on the sign in page. Use the demo account below to log in, which takes you to the protected dashboard:

```
username: admin
password: password123
```

### Running it locally instead

If you want to run it on your own machine, you need PHP 8 or newer:

```bash
cd login
php -S localhost:8000
```

Then open http://localhost:8000 and sign in with the same demo account above.

Deployment notes and the full feature list are in `login/README.md`.

## Tools used

Python, Tkinter, HTML, CSS, JavaScript, PHP.

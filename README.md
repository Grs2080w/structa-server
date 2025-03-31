# Structa Server

## Description

**Structa Server** is a project management server that uses **GraphQL**, **Redis**, and **Flask** to provide a robust and scalable API. It includes features such as **JWT** authentication, two-factor authentication (**OTP**), **PDF** and **CSV** reporting, and support for **SSH key** encryption.

---

## Features

- **JWT Authentication**: Secure tokens for user authentication.
- **OTP Verification**: Sending verification codes via email for two-factor authentication.
- **SSH Encryption**: Using SSH keys to encode and decode JWT tokens.
- **Report Generation**:
- **PDF**: Detailed project reports in PDF format.
- **CSV**: Exporting project data in CSV format.
- **Project Management**:
  - Creating, editing and deleting projects.
  - Adding and removing collaborators.
  - Managing tasks within projects.
- **Redis Database**: Fast and efficient storage of user and project data.

---

## Project Structure

The project structure is organized to facilitate maintenance and scalability:

- `src/`
  - `config/` - Project settings
  - `criptography/` - Encryption and JWT control
  - `flaskr/` - Main implementation of the Flask and GraphQL server
    - `files_exports/` - Report generation (PDF and CSV)
    - `graphql/` - GraphQL schema and resolvers
    - `redis/` - Data control in Redis
  - `otp/` - Sending OTP by email
- `ssh/` - SSH keys for encryption
- `reports/` - Generated reports (PDF and CSV)

<br>

- **[`ssh`](ssh)** folder: Location where SSH keys (`.ssh` and `.ssh.pub`) for encryption should be stored.
- **[`reports`](reports)** folder: Directory where the generated reports (PDF and CSV) are temporarily saved.

---

## Installation

Follow the steps below to configure and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/Grs2080w/structa-server.git
cd structa-server
```

### 2. Create and Activate the Virtual Environment

##### Windows:

```bash

python -m venv .venv
.venv\Scripts\activate
```

##### Linux/MacOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Generate SSH Keys

##### Windows:

1. Open PowerShell or Command Prompt. 2. Run the command:

```bash
ssh-keygen -t rsa -b 2048 -f ssh/.ssh
```

3. Press Enter to accept the default location and enter a password to protect the key.

##### Linux/MacOS:

1. Open the terminal.

2. Run the command:

```bash
ssh-keygen -t rsa -b 2048 -f ssh/.ssh
```

3. Press Enter to accept the default location and enter a password to protect the key.

> **Note:** Make sure that the .ssh (private key) and .ssh.pub (public key) files are saved in the ssh folder in the project root according to the structure.

More about ssh-keygen at: https://www.ssh.com/academy/ssh/keygen

### 4. Configure the `.env` File

Create a `.env` file in the root of the project based on the template provided in `.env.template`. Fill in the environment variables such as `PASSWORD_SSH_KEY`, `REDIS_HOST`, `EMAIL_USER`, etc.

### 5. Install the Dependencies

```bash
pip install -r requirements.txt

```

### 6. Run the Project

To start the server:

```bash
flask --app src/flaskr run
```

Or run the main file directly:

```bash
python src/flaskr/__init__.py
```

## Notes

- Make sure Redis is configured and running before starting the server.
- The generated reports in PDF and CSV are temporarily saved in the reports folder and automatically removed after a period of time.

<br>

You can see more about the API documentation [in this file](API_Documentation.md)

---

With this, the server will be configured and ready to use! 🎉

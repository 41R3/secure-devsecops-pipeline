# Secure DevSecOps Pipeline

This project implements a secure DevSecOps pipeline demonstrating automated security scanning with OWASP ZAP and server hardening using Ansible.

## Project Structure
├── .github/
│   └── workflows/
│       └── devsecops.yml         # GitHub Actions workflow for DevSecOps pipeline
├── ansible/
│   └── playbook.yml              # Ansible playbook for CIS hardening
├── app/
│   ├── init.py               # (Implicit, typical for Flask apps)
│   ├── app.py                    # Flask application
│   ├── error_handlers.py         # Custom error handlers for Flask
│   ├── requirements.txt          # Python dependencies
│   └── wsgi.py                   # WSGI entry point for Gunicorn
├── LICENSE                       # Apache License 2.0
└── README.md                     # This README file

## Features

* **Automated Security Scanning:** Integrates OWASP ZAP for dynamic application security testing (DAST) within the CI/CD pipeline.
* **Server Hardening:** Applies CIS (Center for Internet Security) benchmarks for server hardening using Ansible.
* **Flask Application:** Includes a basic Flask application with enhanced security headers and logging.
* **GitHub Actions:** Orchestrates the entire DevSecOps pipeline, including build, test, security scan, and hardening.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Git
* Docker
* Python 3.x
* Ansible (for local testing of the playbook)

### Installation (Local Development)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/secure-devsecops-pipeline.git](https://github.com/your-username/secure-devsecops-pipeline.git)
    cd secure-devsecops-pipeline
    ```

2.  **Set up the Flask application:**
    ```bash
    cd app
    pip install -r requirements.txt
    ```

3.  **Run the Flask application (for testing):**
    ```bash
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    ```
    The application will be accessible at `http://localhost:5000`. You can test the health check endpoint at `http://localhost:5000/health`.

4.  **Run the Ansible Playbook (for local hardening simulation):**
    ```bash
    cd ansible
    ansible-playbook playbook.yml --connection=local --inventory 127.0.0.1,
    ```
    This will apply the hardening steps to your local machine. **Use with caution on a development machine as it modifies system settings.**

## DevSecOps Pipeline (GitHub Actions)

The `.github/workflows/devsecops.yml` file defines the CI/CD pipeline.

### Workflow Steps:

1.  **`security-scan` Job:**
    * **Checkout Code:** Clones the repository.
    * **Setup Python:** Configures Python 3.10.
    * **Install Dependencies:** Installs Flask application dependencies.
    * **Clean Previous Containers:** Ensures a clean Docker environment.
    * **Start Flask App:** Launches the Flask application using Gunicorn in the background. Includes a health check loop to ensure the app is ready.
    * **Verify Access from Container:** Checks if the Flask app is accessible from a Docker container, simulating how ZAP will connect.
    * **Verify App Status:** Confirms the app is listening on port 5000 and the health check endpoint returns "healthy".
    * **Prepare ZAP Report Directory:** Creates a directory for ZAP reports.
    * **Scan with OWASP ZAP:** Runs a full OWASP ZAP scan against the running Flask application. It generates HTML and Markdown reports. The `SCAN_EXIT_CODE` is captured to determine scan success.
    * **Generate Final Significant Report:** Analyzes the ZAP scan logs and generates a summary message indicating whether vulnerabilities were found or if an error occurred.
    * **Upload ZAP Reports:** Archives and uploads the generated ZAP HTML and Markdown reports as a GitHub Action artifact.

2.  **`server-hardening` Job:**
    * **Depends on `security-scan`:** This job runs only after the `security-scan` job completes (regardless of its success or failure).
    * **Checkout Code:** Clones the repository.
    * **Install Ansible:** Installs Ansible on the runner.
    * **Execute CIS Hardening:** Runs the `ansible/playbook.yml` to apply CIS hardening measures to the server (in this case, the `ubuntu-latest` GitHub Actions runner).
    * **Create Meaningful Report:** Generates a `hardening-report.txt` summarizing the Ansible playbook execution, indicating success or listing detected issues.
    * **Upload Hardening Report:** Archives and uploads the hardening report as a GitHub Action artifact.

## ☕ Apóyame
Si este proyecto te fue útil, considera invitarme un café:  
👉 [ko-fi.com/4er1_](https://ko-fi.com/4er1_)

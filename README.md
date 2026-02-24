# Job–Invoice Reconciliation Automation

This is a Python automation script designed to reconcile completed jobs against issued invoices for a company workflow. The script generates a reconciliation report that flags jobs that are not invoiced or have invoice amount mismatches, and can optionally send the report via email. This script can then be combined with Windows Task Manager for automated scheduling.

**Note: For security reasons, the datasets included in this repository are fully synthetic. No real company data or client information is included.**

## What the Project Does

1. Loads two CSV files:

    - jobs_completed.csv (synthetic jobs data)

    - invoices_issued.csv (synthetic invoices data)

2. Cleans column names for consistency.

3. Merges the datasets on job_id.

4. Flags:

    - Jobs that were completed but not invoiced

    - Jobs where invoice amounts do not match job values

5. Generates a dated reconciliation report:

    - report_DD-MM-YYYY.csv

6. Optionally sends the report via email if Gmail credentials are configured in a .env file.

## Technologies Used

* Python 3

* pandas

* python-dotenv

* smtplib (standard library)

* email.message (standard library)

## Repository Structure

automation/  
│  
├── automation_script_public.py    # The main script  
├── jobs_completed.csv             # Synthetic jobs dataset  
├── invoices_issued.csv            # Synthetic invoices dataset  
├── README.md

**Note: The .env file is not included for security reasons. Please create your own and place it in the same folder to enable email sending.**

## Setup Instructions
**1. Clone the Repository**  
    _git clone <github.com/tinasalihu/automated-reconciliation>_  
    _cd automation_  
   
**2. Create a Virtual Environment (Recommended)**  
    _python3 -m venv venv_  
    _source venv/bin/activate_  
   
**3. Install Dependencies**  
    _pip install pandas python-dotenv_  
   
**4. Create a .env File**   
  Create a .env file in the root directory of the project with the following variables:  

     GMAIL_EMAIL=your_email@gmail.com  
     GMAIL_PASSWORD=your_16_character_app_password  
     RECIPIENT_EMAIL=recipient@gmail.com  

  Where:  

  * GMAIL_EMAIL → your Gmail address

  * GMAIL_PASSWORD → your Gmail App Password (16-character)

  * RECIPIENT_EMAIL → email address where the report will be sent

  If you do not configure the .env file, the script will still generate the report, but email sending will be skipped.  

**5. Running the Script (in terminal)**  
    _python automation_script_public.py_  


The script will:

Generate a reconciliation report with today’s date.

Save it in the project folder as report_DD-MM-YYYY.csv.

Send an email only if all environment variables are configured.

## Report Details

The generated CSV includes the following columns:

* job_id

* client_name

* job_value

* invoice_amount

* not_invoiced → _True_ if job has no invoice

* amount_mismatch → _True_ if invoice amount does not match job value

This allows easy identification of billing discrepancies.

## Future Improvements

- Logging instead of print statements

- Email formatting improvements (HTML email)

- Additional report metrics and analytics


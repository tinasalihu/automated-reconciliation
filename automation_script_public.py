import pandas as pd
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# load the env file to get the sender's email and password, and the recipient email
load_dotenv()
sender_email = os.getenv("GMAIL_EMAIL")
password = os.getenv("GMAIL_PASSWORD")
recipient = os.getenv("RECIPIENT_EMAIL")

# only validate if email sending is enabled
if sender_email and password and recipient:
    receiver_emails = [recipient]
else:
    # if credientials are missing, skip email section
    print("Email credentials not fully configured. Skipping email sending.")

# load the csv files into dataframes
jobs = pd.read_csv("jobs_completed.csv")
invoices = pd.read_csv("invoices_issued.csv")

# clean column names
jobs.columns = jobs.columns.str.strip().str.lower().str.replace(" ", "_")
invoices.columns = invoices.columns.str.strip().str.lower().str.replace(" ", "_")

# merge datasets
merged = jobs.merge(
    invoices,
    on="job_id",  # join on shared column
    how="left"    # left join to keep all completed jobs
)

# flag jobs that have a missing invoice_id
merged["not_invoiced"] = merged["invoice_id"].isna()

# flag jobs where the invoice amount does not match the job value
merged["amount_mismatch"] = (merged["invoice_amount"] != merged["job_value"]) & (~merged["invoice_amount"].isna())

# create report
report = merged[[
    "job_id",
    "client_name",
    "job_value",
    "invoice_amount",
    "not_invoiced",
    "amount_mismatch"
]]

# get today's date
today = datetime.now().strftime("%d-%m-%Y")

# define the report name with today's date
report_csv = f"report_{today}.csv"

# export as csv
report.to_csv(report_csv, index=False)
print(f"Reconciliation report saved as {report_csv}")

# create a summary
total_jobs = len(jobs)  # number of jobs completed
not_invoiced_count = merged["not_invoiced"].sum()   # number of jobs not invoiced
mismatch_count = merged["amount_mismatch"].sum()    # number of amount mismatches

summary_text = f"""
Weekly Job-Invoice Reconciliation Summary (Test)

Total completed jobs: {total_jobs}
Jobs not invoiced: {not_invoiced_count}
Amount mismatches: {mismatch_count}

Please see attached CSV for details.
"""

# define function to send an email report
def send_email(report_csv, summary_text, sender_email, password, recipient):

    msg = EmailMessage()  # initiate email sender
    msg["Subject"] = "Weekly Job-Invoice Reconciliation (Test)"  # define subject line
    msg["From"] = sender_email  # define sender
    msg["To"] = recipient  # define recipient
    msg.set_content(summary_text)  # define content


    # attach csv report to email
    with open(report_csv, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=report_csv,
        )

    # send using Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)


# if credentials exist, call the function to send an email
if sender_email and password and recipient:
    send_email(report_csv, summary_text, sender_email, password, recipient)
    print("Reconciliation email sent successfully!")

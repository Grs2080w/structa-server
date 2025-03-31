import csv
import os
import threading
import time

from flask import Flask, send_file
from flask_cors import CORS
from fpdf import FPDF, HTMLMixin
from mistletoe import markdown

from flaskr.files_exports.report_pdf import text_for_pdf
from flaskr.files_exports.utils.format_project_data import data_format
from flaskr.files_exports.utils.project_by_id import (
    get_project_by_id_and_user_is_creator,
)
from flaskr.graphql.server import graphql_Blueprint

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST"],
)

# dir for manage the reports
os.makedirs("reports", exist_ok=True)


# function do remove the file
def remove_file_later(file_path, delay=5):
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")


class PDF(FPDF, HTMLMixin):
    pass


@app.route("/download/csv/<project_id>/<token>")
def download_csv(project_id, token):
    file_path = f"C:/Users/Gabriel Santos/workspace/orgpro-app-server/reports/report_{project_id}.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    project = get_project_by_id_and_user_is_creator(project_id, token)

    if project.get("code"):
        return project

    data = data_format(project, type="csv")

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    threading.Thread(target=remove_file_later, args=(file_path,)).start()

    return send_file(file_path, as_attachment=True)


@app.route("/download/pdf/<project_id>/<token>")
def download_pdf(project_id, token):
    file_path = file_path = (
        f"C:/Users/Gabriel Santos/workspace/orgpro-app-server/reports/report_{project_id}.pdf"
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    project = get_project_by_id_and_user_is_creator(project_id, token)

    if project.get("code"):
        return project

    data = data_format(project, type="pdf")
    html = markdown(text_for_pdf(data))
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    pdf.write_html(html)
    pdf.output(file_path)

    threading.Thread(target=remove_file_later, args=(file_path, 10)).start()

    return send_file(file_path, as_attachment=True)


# Blueprint
app.register_blueprint(graphql_Blueprint)

if __name__ == "__main__":
    app.run()

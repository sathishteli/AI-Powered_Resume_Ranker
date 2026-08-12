import io

from app.web_app import app


def test_home_page_loads():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_empty_job_description():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "job_description": "",
        },
    )

    assert response.status_code == 200

    assert (
        b"Job description is empty"
        in response.data
    )


def test_no_resumes_uploaded():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "job_description": (
                "Python Machine Learning Engineer"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        b"No resumes were uploaded"
        in response.data
    )


def test_non_pdf_upload_rejected():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "job_description": (
                "Python Machine Learning Engineer"
            ),
            "resumes": (
                io.BytesIO(
                    b"Sample resume"
                ),
                "resume.txt",
            ),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200

    assert (
        b"Only PDF resumes are supported"
        in response.data
    )


def test_download_report_without_results():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/download-report"
    )

    assert response.status_code == 400

    assert (
        b"No ranking results available"
        in response.data
    )


def test_download_pdf_report_without_results():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/download-pdf-report"
    )

    assert response.status_code == 400

    assert (
        b"No ranking results available"
        in response.data
    )
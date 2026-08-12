import io

from app.web_app import (
    app,
    create_app,
)


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


def test_create_app_default_configuration():

    application = create_app()

    assert (
        application.config["MAX_CONTENT_LENGTH"]
        == 10 * 1024 * 1024
    )

    assert (
        application.config["MAX_RESUME_FILES"]
        == 10
    )

    assert (
        application.config["MAX_RESUME_SIZE"]
        == 5 * 1024 * 1024
    )

    assert (
        application.config["FLASK_HOST"]
        == "127.0.0.1"
    )

    assert (
        application.config["FLASK_PORT"]
        == 5000
    )

    assert (
        application.config["FLASK_DEBUG"]
        is True
    )


def test_request_too_large_handler():

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
                    b"x"
                ),
                "resume.pdf",
            ),
        },
        content_type="multipart/form-data",
    )

    # This test confirms that the application
    # continues to accept normal-sized requests.
    assert response.status_code != 413


def test_custom_application_configuration(
    monkeypatch,
):

    monkeypatch.setenv(
        "FLASK_SECRET_KEY",
        "test-secret-key",
    )

    monkeypatch.setenv(
        "FLASK_DEBUG",
        "false",
    )

    monkeypatch.setenv(
        "FLASK_HOST",
        "0.0.0.0",
    )

    monkeypatch.setenv(
        "FLASK_PORT",
        "5050",
    )

    monkeypatch.setenv(
        "MAX_CONTENT_LENGTH_MB",
        "20",
    )

    monkeypatch.setenv(
        "MAX_RESUME_FILES",
        "25",
    )

    monkeypatch.setenv(
        "MAX_RESUME_SIZE_MB",
        "8",
    )

    application = create_app()

    assert (
        application.secret_key
        == "test-secret-key"
    )

    assert (
        application.config["FLASK_DEBUG"]
        is False
    )

    assert (
        application.config["FLASK_HOST"]
        == "0.0.0.0"
    )

    assert (
        application.config["FLASK_PORT"]
        == 5050
    )

    assert (
        application.config["MAX_CONTENT_LENGTH"]
        == 20 * 1024 * 1024
    )

    assert (
        application.config["MAX_RESUME_FILES"]
        == 25
    )

    assert (
        application.config["MAX_RESUME_SIZE"]
        == 8 * 1024 * 1024
    )
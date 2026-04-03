import os


UPLOAD_DIR = "/var/www/uploads"


def serve_file(filename):
    # BUG: no sanitization of filename, allows ../../etc/passwd
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, 'r') as f:
        return f.read()


def handle_request(request):
    filename = request.get("file")
    if not filename:
        return "No file specified"
    return serve_file(filename)

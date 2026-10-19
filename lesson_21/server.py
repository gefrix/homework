"""Простой HTTP-сервер для домашней работы 21.2."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HOST = "localhost"
PORT = 8080
BASE_DIR = Path(__file__).resolve().parent


def read_html(filename: str) -> str:
    """Прочитать HTML-файл в кодировке UTF-8."""
    with open(BASE_DIR / filename, "r", encoding="utf-8") as file:
        return file.read()


class HomeworkRequestHandler(BaseHTTPRequestHandler):
    """Обработчик GET- и POST-запросов домашнего веб-приложения."""

    def send_html(self, status_code: int, html: str) -> None:
        response = html.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:
        """На любой GET-запрос вернуть страницу «Контакты»."""
        try:
            self.send_html(200, read_html("contacts.html"))
        except OSError as error:
            print(f"Не удалось прочитать страницу: {error}")
            self.send_html(500, read_html("500.html"))

    def do_POST(self) -> None:
        """Принять форму, вывести данные в консоль и показать результат."""
        path = urlparse(self.path).path
        if path not in {"/", "/contacts", "/contacts.html"}:
            self.send_html(404, read_html("404.html"))
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            request_body = self.rfile.read(content_length).decode("utf-8")
            form_data = parse_qs(request_body, keep_blank_values=True)

            print("Получены данные POST-запроса:")
            for field_name, values in form_data.items():
                print(f"{field_name}: {', '.join(values)}")

            feedback = """
            <div class="alert alert-success" role="alert">
                Спасибо! Ваше сообщение принято.
            </div>
            """
            contacts_page = read_html("contacts.html").replace(
                "<!-- feedback -->", feedback
            )
            self.send_html(200, contacts_page)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            print(f"Ошибка обработки POST-запроса: {error}")
            self.send_html(500, read_html("500.html"))


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), HomeworkRequestHandler)
    print(f"Сервер запущен: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Сервер остановлен.")

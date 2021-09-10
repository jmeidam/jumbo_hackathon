from flask import Flask, request


class Product:
    def __init__(self, parameter1, parameter2, package):
        self.parameter1 = parameter1
        self.parameter2 = parameter2
        self.package = package

    def get_green_score(self):
        return self.parameter1 + self.parameter2


class Receipt:
    def __init__(self, products):
        self.products = products

    def add_products(self, products):
        self.products.append(products)

    def calculate_green_score(self):
        score = 0
        for product in self.products:
            score += product.get_green_score()
        return score


app = Flask(__name__)


@app.route("/")
def whatever():
    value = 5
    return f"<p>Test = {value}</p>"


@app.route('/post_test/', methods=['POST'])
def post_test():
    content = request.get_json()
    print(content)

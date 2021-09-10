from flask import Flask, request


class Product:
    def __init__(self, ean: int, distance: float, package: int, production_cost: int):
        self.ean = ean
        self.distance = distance  # logistical distance in km
        self.package = package
        self.prod_cost = production_cost

        print(f'creating product aen: {self.ean}')

    def get_green_score(self) -> float:
        return self.prod_cost + self.package/1.25 + self.distance/20


class Receipt:
    def __init__(self, products: list = None):
        if not products:
            self.products = []
        else:
            self.products = products

    def add_product(self, product: Product):
        self.products.append(product)

    def calculate_total_green_score(self):
        score_tot = 0
        for product in self.products:
            score = product.get_green_score()
            print(f'debug: score for product {product.ean} is {score}')
            score_tot += score
        return score_tot/len(self.products)


def parse_item(item: dict) -> dict:
    params = {
        'ean': int(item['EAN']),
        'distance': float(item['logisticalDistance'].replace('km', '')),
        'package': int(item['verpakking']),
        'production_cost': int(item['productieImpact'])
    }
    return params


app = Flask(__name__)


@app.route("/")
def just_a_message():
    return f"<p>API is live</p>"


@app.route('/score_receipt/', methods=['POST'])
def score_receipt():
    content = request.get_json()
    receipt = Receipt()
    for item in content['products']:
        params = parse_item(item)
        receipt.add_product(Product(**params))

    return {'score': receipt.calculate_total_green_score()}


@app.route('/score_product/', methods=['POST'])
def score_product():
    content = request.get_json()
    params = parse_item(content)
    product = Product(**params)

    return {'score': product.get_green_score()}

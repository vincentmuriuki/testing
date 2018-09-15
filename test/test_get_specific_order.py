import unittest 
import json
from app import app


with open('orders.json') as orders_json:
    orders = json.load(orders_json)
class TestFlaskApi(unittest.TestCase):
    """
    Test the fast food fast order api endpoints
    """

    def setUp(self):
        """ setting up the setup of the test and variable """
        self.app = app.test_client()

        self.new_order = {
            "user_name":"Philip Otieno",
            "products":{
                "name":"Chips Bhajia",
                "qty":4,
                "price":400
            }
        }

        self.existing_order_id = 1

        self.nonexisting_order_id = 5
    def test_get_specific_order(self):
            
            response = self.app.get(
                '/api/v1/orders/{}/'.format(self.existing_order_id),
                content_type = "application/json"
            )

            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
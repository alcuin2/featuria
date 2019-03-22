import unittest
from featuria import db, bcrypt
from featuria.models import User, Client, Feature, PriorityRange, ProductArea


class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        hashed_password = bcrypt.generate_password_hash("qwerty123456").decode("utf-8")
        cls.user = User(fullname="John Doe", email="johndoe@email.com", password=hashed_password)
        db.session.add(cls.user)
        db.session.commit()
        user = User.query.filter_by(email="johndoe@email.com").first()
        cls.client = Client(name="Client A", added_by=user.id)
        db.session.add(cls.client)
        db.session.commit()
        cls.priority_range = PriorityRange(range=10)
        cls.product_area = ProductArea(title="Policies", added_by=user.id)
        cls.feature1 = Feature(title="Sample1", description="sample description", client_id=cls.client.id,
                               priority=1, product_area="Policies", target_date="2019-03-30", added_by=user.id)

        db.session.add(cls.priority_range)
        db.session.add(cls.product_area)
        db.session.add(cls.feature1)
        db.session.add(cls.feature2)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        db.create_all()

    def test_user(self):
        user = User.query.get(1)
        self.assertEqual(user.fullname, "John Doe")
        self.assertEqual(user.email, "johndoe@email.com")

    def test_priority_range(self):
        self.assertEqual(self.priority_range.range, 10)

    def test_features(self):
        feature = Feature.query.get(1)
        user = User.query.get(1)
        self.assertEqual(feature.client_id, self.client.id)
        self.assertEqual(feature.added_by, user.id)


if __name__ == "__main__":
    unittest.main()

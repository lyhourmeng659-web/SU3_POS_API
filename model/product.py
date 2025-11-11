from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)

    # SQLAlchemy relationship
    category = db.relationship("Category", back_populates="products")

    def to_dict(self, include_category=False):
        data = {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "cost": self.cost,
            "price": self.price,
            "image": self.image
        }
        if include_category and self.category:
            data["category"] = self.category.to_dict()
        return data

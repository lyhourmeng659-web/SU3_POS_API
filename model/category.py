from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image = db.Column(db.String(255), nullable=True)

    # backref allows Category.products to list all products in the category
    products = db.relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image
        }

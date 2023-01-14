from sqlalchemy.orm import Session
from typing import List, Optional

from ecommerce_api.sql import models
from ecommerce_api.schemas import User, Product
from ecommerce_api.sql.database import database_operation
from ecommerce_api.errors import NotFound
from ecommerce_api.enums import OrderStatus


class UserOperations:

    @database_operation
    def create(self, db: Session, user: User) -> models.User:
        new_user = models.User(
            email=user.email,
            password=user.password,
            type=user.type
        )
        db.add(new_user)
        db.commit()
        return new_user

    @database_operation
    def get_by_email(self, db: Session, email: str) -> Optional[models.User]:
        user = db.query(models.User).filter(
            models.User.email == email
        ).first()
        return user

    @database_operation
    def get_all(self, db: Session) -> Optional[List[models.User]]:
        all_users = db.query(models.User).all()
        return all_users

    @database_operation
    def delete(self, db: Session, email: str) -> None:
        db.query(models.User).filter(models.User.email == email).delete()
        db.commit()


class ProductOperations:

    @database_operation
    def create(self, db: Session, product: Product) -> models.Product:
        db.add(**product.dict())
        db.commit()
        return product

    @database_operation
    def get_all(self, db: Session) -> Optional[List[models.Product]]:
        all_products = db.query(models.Product).all()
        return all_products

    @database_operation
    def get_by_id(
            self,
            db: Session,
            product_id: str
    ) -> Optional[models.Product]:
        product = db.query(models.Product).filter(
            models.Product.id == product_id
        ).first()
        return product

    @database_operation
    def get_by_category(
            self,
            db: Session,
            category: str
    ) -> Optional[List[models.Product]]:
        matching_products = db.query(models.Product).filter(
            models.Product.category == category
        ).all()
        return matching_products

    @database_operation
    def update(
            self,
            db: Session,
            product_id: str,
            product: Product
    ) -> models.Product:
        db.query(models.Product).filter(
            models.Product.id == product_id
        ).update(**product.dict())
        db.commit()
        return product

    @database_operation
    def remove(self, db: Session, product_id: str) -> None:
        db.query(models.Product).filter(
            models.Product.id == product_id
        ).delete()
        db.commit()


class OrderOperations:

    @database_operation
    def add_to_order(self, db: Session, email: str, product_id: str) -> None:
        product = db.query(models.Product).get(product_id)
        if not product:
            raise NotFound(details="Product not found")
        if product.quantity <= 0:
            raise NotFound(details="Product out of stock")
        order = db.query(models.Order).filter(
            models.Order.user_email == email
        ).first()
        if not order:
            new_order = models.Order(user_email=email)
            current_quantity = product.first().quantity - 1
            product.update({"quantity": current_quantity})
            db.add(new_order)
            db.commit()
        else:
            current_quantity = product.first().quantity - 1
            product.update({"quantity": current_quantity})
            db.commit()

    @database_operation
    def get_all_items(self, db: Session, email: str) -> models.Order:
        order = db.query(models.Order).filter(
            models.Order.user_email == email
        ).first()
        return order

    @database_operation
    def remove_item(self, db: Session, email: str, product_id: str) -> None:
        order = db.query(models.Order).filter(
            models.User.email == email
        ).first()
        db.query(models.Order).filter(
            models.Order.products.id == product_id
        ).delete()
        db.commit()

    @database_operation
    def submit(self, db: Session, email: str) -> models.Order:
        order = db.query(models.Order).filter(
            models.User.email == email
        ).first()

        if not order.count():
            raise NotFound(details="No items in cart")

        total_price: float = 0.0
        for item in order.products:
            total_price += item.price

        new_order = models.Order(
            total_price=total_price,
            user_email=email,
            status=OrderStatus.SUBMITTED
        )
        db.add(new_order)
        db.commit()
        return new_order

    @database_operation
    def get_orders(self, db: Session, email: str = None) -> List[models.Order]:
        if not email:
            return db.query(models.Order).all()
        orders = db.query(models.Order).filter(
            models.Order.customer_email == email
        ).all()
        return orders

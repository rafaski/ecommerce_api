from sqlalchemy.orm import Session
from typing import List, Optional

from ecommerce_api.sql import models
from ecommerce_api.schemas import User, Product
from ecommerce_api.sql.database import database_operation
from ecommerce_api.errors import NotFound
from ecommerce_api.enums import OrderStatus
from ecommerce_api.auth.password import to_hash


class UserOperations:
    """
    Database operations on User class (SQL table)
    """

    @database_operation
    def create(self, db: Session, user: User) -> None:
        """Create new user"""
        user.password = to_hash(user.password)
        db.add(**user.dict())
        db.commit()

    @database_operation
    def get_by_email(self, db: Session, email: str) -> Optional[models.User]:
        """Get user by email"""
        user = db.query(models.User).filter(
            models.User.email == email
        ).first()
        return user

    @database_operation
    def get_all(self, db: Session) -> Optional[List[models.User]]:
        """Get all users from db"""
        all_users = db.query(models.User).all()
        return all_users

    @database_operation
    def delete(self, db: Session, email: str) -> None:
        """Delete a user"""
        db.query(models.User).filter(models.User.email == email).delete()
        db.commit()


class ProductOperations:
    """
    Database operations on Product class (SQL table)
    """

    @database_operation
    def create(self, db: Session, product: Product) -> None:
        """Create a product"""
        db.add(**product.dict())
        db.commit()

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
        """Get product by id"""
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
        """Get product by category"""
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
        """Update product"""
        updated_product = db.query(models.Product).filter(
            models.Product.id == product_id
        ).update(**product.dict())
        db.commit()
        return updated_product

    @database_operation
    def remove(self, db: Session, product_id: str) -> None:
        """Delete product from db"""
        db.query(models.Product).filter(
            models.Product.id == product_id
        ).delete()
        db.commit()


class OrderOperations:
    """
    Database operations on Order class (SQL table)
    """

    @database_operation
    def add(
        self,
        db: Session,
        email: str,
        order_id: str,
        product_id: str
    ) -> None:
        """Add product to cart"""
        product = db.query(models.Product).get(product_id).first()
        product.update({"quantity": product.quantity - 1})

        order = db.query(models.Order).filter(
            models.Order.id == order_id
        ).first()
        if not order:
            order = models.Order(user_email=email, products=[product_id])
            db.add(order)
        else:
            order.products.append(product_id)
        order.total_price += product.price
        db.commit()

    @database_operation
    def get(self, db: Session, order_id: str) -> models.Order:
        """Get order (all items in cart)"""
        order = db.query(models.Order).filter(
            models.Order.id == order_id
        ).all()
        return order

    @database_operation
    def get_all(self, db: Session, email: str = None) -> List[models.Order]:
        """Get all orders from db"""
        if not email:
            return db.query(models.Order).all()
        orders = db.query(models.Order).filter(
            models.Order.customer_email == email
        ).all()
        return orders

    @database_operation
    def remove_item(self, db: Session, order_id: str, product_id: str) -> None:
        """Remove an item from order (cart)"""
        order = db.query(models.Order).filter(
            models.Order.id == order_id
        ).first()
        if product_id not in order.products:
            return
        product = db.query(models.Product).get(product_id).first()
        product.update({"quantity": product.quantity + 1})
        order.products.remove(product_id)
        db.commit()

    @database_operation
    def submit(self, db: Session, order_id: str) -> models.Order:
        """Submit an order (finalize cart)"""
        order = db.query(models.Order).filter(
            models.Order.id == order_id
        ).first()

        if not order.products:
            raise NotFound(details="No items in cart")

        order.status = OrderStatus.SUBMITTED
        db.add(order)
        db.commit()
        return order

    @database_operation
    def cancel(self, db: Session, order_id: str) -> None:
        """Cancel (delete) order"""
        order = db.query(models.Order).filter(
            models.Order.id == order_id
        ).first()
        for product_id in order.products:
            product = db.query(models.Product).get(product_id).first()
            product.update({"quantity": product.quantity + 1})

        order.delete()
        db.commit()



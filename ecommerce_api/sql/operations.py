from sqlalchemy.orm import Session
from typing import List, Optional

from ecommerce_api.sql import models
from ecommerce_api.schemas import User, Product, ShowCart
from ecommerce_api.sql.database import database_operation
from ecommerce_api.errors import NotFound


# models.User operations
@database_operation
async def get_user_by_email(db: Session, email: int) -> Optional[models.User]:
    user = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    return user


@database_operation
async def get_users(db: Session) -> Optional[List[models.User]]:
    all_users = await db.query(models.User).all()
    return all_users


@database_operation
async def create_user(db: Session, user: User) -> models.User:
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    await db.add(new_user)
    await db.commit()
    return new_user


@database_operation
async def remove_user(db: Session, email: str) -> None:
    await db.query(models.User).filter(models.User.email == email).delete()
    await db.commit()


# models.Product operations
@database_operation
async def get_all_products(db: Session) -> Optional[List[models.Product]]:
    all_products = await db.query(models.Product).all()
    return all_products


@database_operation
async def get_product_by_id(
        db: Session,
        product_id: str
) -> Optional[models.Product]:
    product = await db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    return product


@database_operation
async def get_products_by_category(
        db: Session,
        category: str
) -> Optional[List[models.Product]]:
    matching_products = await db.query(models.Product).filter(
        models.Product.category == category
    ).all()
    return matching_products


@database_operation
async def create_product(db: Session, product: Product) -> models.Product:
    new_product = models.Product(
        id=product.product_id,
        name=product.name,
        quantity=product.quantity,
        category=product.category,
        description=product.description,
        price=product.price,
        date_posted=product.created_date
    )
    await db.add(new_product)
    await db.commit()
    return new_product


@database_operation
async def update_product(
        db: Session,
        product_id: str,
        product: Product
) -> models.Product:
    updated_product = models.Product(
        id=product.product_id,
        name=product.name,
        quantity=product.quantity,
        category=product.category,
        description=product.description,
        price=product.price,
        date_posted=product.created_date
    )
    await db.query(models.Product).filter(
        models.Product.id == product_id
    ).update(**updated_product.dict())
    await db.commit()
    return updated_product


@database_operation
async def remove_product(db: Session, product_id: str) -> None:
    await db.query(models.Product).filter(
        models.Product.id == product_id
    ).delete()
    await db.commit()


# models.Cart operations
@database_operation
async def add_to_cart(db: Session, email: str, product_id: str) -> None:
    product_info = await db.query(models.Product).get(product_id)
    if not product_info:
        raise NotFound(details="Product not found")
    if product_info.quantity <= 0:
        raise NotFound(details="Product out of stock")
    user_info = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    cart_info = await db.query(models.Cart).filter(
        models.Cart.user_email == user_info.email
    ).first()
    if not cart_info:
        new_cart = models.Cart(user_email=user_info.email)
        await db.add(new_cart)
        await db.commit()
        await add_items_to_cart(
            cart_id=new_cart.id,
            product_id=product_info.id,
            db=db
        )
    else:
        await add_items_to_cart(
            cart_id=cart_info.id,
            product_id=product_info.id,
            db=db
        )


@database_operation
async def add_items_to_cart(db: Session, cart_id: str, product_id: str) -> None:
    cart_items = models.CartItems(cart_id=cart_id, product_id=product_id)
    await db.add(cart_items)
    await db.commit()


@database_operation
async def get_all_items_in_cart(db: Session, email: str) -> models.Cart:
    user_info = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    cart = await db.query(models.Cart).filter(
        models.Cart.user_email == user_info.email
    ).first()
    return cart


@database_operation
async def remove_cart_item(db: Session, email: str, cart_item_id: str) -> None:
    user_info = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    cart_id = await db.query(models.Cart).filter(
        models.User.email == user_info.email
    ).first()
    await db.query(models.CartItems).filter(
        models.CartItems.id == cart_item_id,
        models.CartItems.cart_id == cart_id.id
    ).delete()
    await db.commit()


# models.Order operations
@database_operation
async def make_order(db: Session, email: str) -> models.Order:
    user_info = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    cart = await db.query(models.Cart).filter(
        models.Cart.user_email == user_info.email
    ).first()

    cart_items_objects = await db.query(models.CartItems).filter(
        models.Cart.id == cart.id
    )
    if not cart_items_objects.count():
        raise NotFound(details="No items in cart")

    total_amount: float = 0.0
    for item in cart_items_objects:
        total_amount += item.products.price

    new_order = models.Order(
        order_total=total_amount,
        customer_email=user_info.email
    )
    await db.add(new_order)
    await db.commit()

    order_details_objects = []
    for item in cart_items_objects:
        new_order_details = models.OrderDetails(
            order_id=new_order.id,
            product_id=item.products.id
        )
        order_details_objects.append(new_order_details)
    await db.bulk_save_objects(order_details_objects)
    await db.commit()

    await db.query(models.CartItems).filter(
        models.CartItems.cart_id == cart.id
    ).delete()
    await db.commit()

    return new_order


@database_operation
async def get_all_user_orders(db: Session, email: str) -> List[models.Order]:
    user_info = await db.query(models.User).filter(
        models.User.email == email
    ).first()
    orders = await db.query(models.Order).filter(
        models.Order.customer_email == user_info.email
    ).all()
    return orders


@database_operation
async def get_all_orders(db: Session) -> List[models.Order]:
    orders = await db.query(models.Order).all()
    return orders

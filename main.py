from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from engine import session_factory
from sql_schemas import User, Address, Product, Order


def print_users(session: Session):
    for user in get_users(session):
        print(user.username)

def get_users(session: Session):
    query = select(User).options(selectinload(User.addresses))
    users = session.execute(query).scalars().all()
    return users

def get_addresses(session: Session):
    query = select(Address)
    addresses = session.execute(query).scalars().all()
    return addresses

def get_products(session: Session):
    query = select(Product)
    products = session.execute(query).scalars().all()
    return products

def add_users(session: Session):
    users = [
        User(username="John Doe", email="jdoe@example.com"),
        User(username="Alice Smith", email="alice@example.com"),
        User(username="Bob Johnson", email="bob@example.com"),
        User(username="Carol Davis", email="carol@example.com"),
        User(username="Nikita Osminin", email="n.osminin@example.com")
    ]
    for user in users:
        session.add(user)
    session.commit()

def add_addresses(session: Session):
    users = get_users(session)
    addresses = [
        Address(user=users[0], country='Russia', city='Moscow', street='Zhukov'),
        Address(user=users[1], country='Russia', city='Saint Petersburg', street='Lomonosov'),
        Address(user=users[2], country='Russia', city='Yekaterinburg', street='Kraulya'),
        Address(user=users[3], country='Russia', city='Yevpatoriya', street='Chapaev'),
        Address(user=users[4], country='Russia', city='Chelyabinsk', street='Tversk'),
    ]
    for address in addresses:
        session.add(address)
    session.commit()

def add_products(session: Session):
    products = [
        Product(name = 'apple', price = 5.99),
        Product(name = 'banana', price = 2),
        Product(name = 'vinegar', price = 5),
        Product(name = 'pineapple', price = 6),
        Product(name = 'grape', price = 1),
        Product(name = 'matches', price = 3),
    ]
    for product in products:
        session.add(product)
    session.commit()

def add_orders(session: Session):
    users = get_users(session)
    addresses = get_addresses(session)
    products = get_products(session)
    orders = [
        Order(user=users[0], address=addresses[0], product=products[0]),
        Order(user=users[1], address=addresses[1], product=products[1]),
        Order(user=users[2], address=addresses[2], product=products[2]),
        Order(user=users[3], address=addresses[3], product=products[3]),
        Order(user=users[4], address=addresses[4], product=products[4]),
    ]
    for order in orders:
        session.add(order)
    session.commit()

with session_factory() as session:
    print()
    # add_users(session)
    # print_users(session)
    # add_addresses(session)
    # add_products(session)
    # add_orders(session)
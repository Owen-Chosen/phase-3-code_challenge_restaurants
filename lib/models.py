from sqlalchemy import String, Integer, ForeignKey, Column, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Restaurant(Base):
    _tablename_ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref='restaurant')
    customers = relationship ('Customer', secondary='reviews', back_populates='restaurants')


    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self):
        all_review_list = []
        for review in self.reviews:
            customer_name = f"Name:{review.customer}, {review.customer.last_name}"
            string_review = f"Review for {self.name} by {customer_name}: {review.rating} stars."
            all_review_list.append(string_review)

        return all_review_list

class Customer(Base):
    _tablename_ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', backref='customer') 
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def full_name(self):
        return f"First Name:{self.first_name} Last Name:{self.last_name}"
    
    def favorite_restaurant(self):
        max_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.rating > max_rating:
                max_rating = review.rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant

    def add_review(self,restaurant, rating):
        new_review = Review(restaurant=restaurant, rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
       
        delete_reviews = [review for review in self.reviews if review.restaurant == restaurant]

        for review in delete_reviews:
            session.delete(review)
        session.commit()



class Review(Base):
    _tablename_ = 'reviews'

    id = Column(Integer(), primary_key=True)
    restaurant_id = Column(Integer())
    customer_id = Column(Integer())

    restaurant_iden = Column(Integer(), ForeignKey('restaurants.id'))
    customer_iden = Column(Integer(), ForeignKey('customers.id'))



    def full_review(self):
        return f"Review for: {self.restaurant.name} by {self.full_name()}: {self.rating} stars"
    




engine = create_engine('sqlite:///many_to_many.db', echo=True)
Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind=engine)
session = Session()
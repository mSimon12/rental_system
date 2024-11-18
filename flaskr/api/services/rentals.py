from datetime import datetime
from flaskr.api.models.rentals import Rentals


class RentalsService:

    @staticmethod
    def get_rent_match(item_id, user_id):
        return Rentals.query_match_item_user(item_id, user_id)

    @staticmethod
    def associate_user_to_rent(item_id, user_id):
        rent_info = { 'item_id': item_id,
                      'user_id': user_id,
                      'date': datetime.now().date()

        }

        return Rentals.add_item_user_link(rent_info)

    @staticmethod
    def disassociate_user_from_rent(rent_id):
        return Rentals.update_item_user_link(rent_id, datetime.now().date())
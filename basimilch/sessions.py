from django.contrib import messages
from juntagrico_custom_sub.util.sessions import SignupManager as CustomSubSignupManager

from basimilch.depot_rules import depot_allows, error_message


class SignupManager(CustomSubSignupManager):
    def get_next_page(self):
        # every signup step checks the next page, so this also catches depots selected via the map,
        # manipulated requests or subscription types changed after the depot was selected
        depot = self.depot()
        if depot is not None and not depot_allows(depot, self.subscriptions()):
            self.set('depot', None)
            messages.error(self.request, error_message(depot) + ' Bitte wähle ein anderes Depot.')
        return super().get_next_page()

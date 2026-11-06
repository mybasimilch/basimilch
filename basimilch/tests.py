from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import resolve, reverse
from juntagrico.entity.subtypes import SubscriptionCategory
from juntagrico.forms import SubscriptionPartChangeForm, SubscriptionPartOrderForm
from juntagrico.tests import JuntagricoTestCase

from basimilch.depot_rules import depot_allows
from basimilch.models import DepotDeliveryOptions
from basimilch.sessions import SignupManager


class DepotIntervalTestCase(JuntagricoTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # bundle without 2/4/8 liter sizes, so basimilch's quantity validation does not interfere
        category = SubscriptionCategory.objects.create(name='interval_category')
        bundle = cls.create_bundle('interval_bundle', category)
        cls.weekly_type = cls.create_sub_type(bundle, shares=0)
        cls.biweekly_type = cls.create_sub_type(bundle, shares=0, interval=2)
        # depot2 allows longer intervals, depot does not
        DepotDeliveryOptions.objects.create(depot=cls.depot2, allows_longer_intervals=True)
        cls.weekly_sub = cls.create_sub_now(cls.depot, parts=[cls.weekly_type])
        cls.member4.join_subscription(cls.weekly_sub, True)


class DepotRulesTest(DepotIntervalTestCase):
    def test_depot_allows(self):
        self.assertTrue(depot_allows(self.depot, [self.weekly_type]))
        self.assertFalse(depot_allows(self.depot, [self.weekly_type, self.biweekly_type]))
        self.assertTrue(depot_allows(self.depot2, [self.biweekly_type]))

    def test_admin_inline(self):
        response = self.assertGet(reverse('admin:juntagrico_depot_change', args=[self.depot.pk]), member=self.admin)
        self.assertContains(response, 'Längere Lieferintervalle erlaubt')


class SignupTest(DepotIntervalTestCase):
    def test_signup_manager_is_configured(self):
        from juntagrico.config import Config
        self.assertEqual(Config.signup_manager(), 'basimilch.sessions.SignupManager')

    def get_signup_manager(self, subscription_type, depot):
        request = RequestFactory().get(reverse('cs-start'))
        SessionMiddleware(lambda r: None).process_request(request)
        MessageMiddleware(lambda r: None).process_request(request)
        request.user = AnonymousUser()
        request.resolver_match = resolve(reverse('cs-start'))
        manager = SignupManager(request)
        manager.set('main_member', {'email': 'new@email.org'})
        manager.set('subscriptions', {str(subscription_type.pk): 1})
        manager.set('depot', str(depot.pk))
        return manager

    def test_invalid_depot_is_reset(self):
        manager = self.get_signup_manager(self.biweekly_type, self.depot)
        manager.get_next_page()
        self.assertIsNone(manager.get('depot'))
        self.assertEqual(len(get_messages(manager.request)), 1)

    def test_valid_depots_are_kept(self):
        for sub_type, depot in [(self.biweekly_type, self.depot2), (self.weekly_type, self.depot)]:
            manager = self.get_signup_manager(sub_type, depot)
            manager.get_next_page()
            self.assertEqual(manager.get('depot'), str(depot.pk))
            self.assertEqual(len(get_messages(manager.request)), 0)

    def render_select(self, subscription_type):
        return render_to_string('juntagrico/snippets/depot/select.html', {
            'depots': [self.depot, self.depot2],
            'subscription_count': {str(subscription_type.pk): 1},
            'selected': self.depot.pk,
        })

    def test_select_disables_depot(self):
        html = self.render_select(self.biweekly_type)
        self.assertInHTML(f'<option value="{self.depot.pk}" id="depot{self.depot.sort_order}" disabled>'
                          f'{self.depot.name} (nur wöchentliche Lieferung)</option>', html)
        self.assertNotIn('selected', html)

    def test_select_without_longer_interval(self):
        html = self.render_select(self.weekly_type)
        self.assertNotIn('disabled', html)
        self.assertIn('selected', html)

    def test_select_with_integer_keys(self):
        # the depot change page passes the current types of the subscription with integer keys
        html = render_to_string('juntagrico/snippets/depot/select.html', {
            'depots': [self.depot], 'subscription_count': {self.biweekly_type.pk: 1},
        })
        self.assertIn('disabled', html)


class PartValidatorTest(DepotIntervalTestCase):
    def assertDepotError(self, form, expected=True):
        form.is_valid()
        codes = [e.code for e in form.non_field_errors().as_data()]
        self.assertEqual('depot_interval' in codes, expected, form.errors)

    def test_order(self):
        self.assertDepotError(SubscriptionPartOrderForm(self.weekly_sub, {f'amount[{self.biweekly_type.pk}]': 1}))
        self.assertDepotError(SubscriptionPartOrderForm(self.weekly_sub, {f'amount[{self.weekly_type.pk}]': 1}),
                              expected=False)

    def test_order_at_allowed_depot(self):
        self.weekly_sub.depot = self.depot2
        self.weekly_sub.save()
        self.assertDepotError(SubscriptionPartOrderForm(self.weekly_sub, {f'amount[{self.biweekly_type.pk}]': 1}),
                              expected=False)

    def test_order_with_pending_depot_change(self):
        self.weekly_sub.depot = self.depot2
        self.weekly_sub.future_depot = self.depot
        self.weekly_sub.save()
        self.assertDepotError(SubscriptionPartOrderForm(self.weekly_sub, {f'amount[{self.biweekly_type.pk}]': 1}))

    def test_change(self):
        part = self.weekly_sub.parts.get()
        self.assertDepotError(SubscriptionPartChangeForm(part, {'part_type': self.biweekly_type.pk}))

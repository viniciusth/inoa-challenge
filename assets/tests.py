from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Asset
from .forms import UserCreationForm, EditUserForm, TickerField, TrackAssetForm, RemoveTrackedAssetForm, GraphPeriodForm 

class TestHomeView(TestCase):
  def test_get(self):
    resp = self.client.get('', {})
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="home.html")
    self.assertEqual(resp.status_code, 200)
    
class TestProfileView(TestCase):
  def test_get(self):
    resp = self.client.get('/profile/', {})
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="profile.html")
    self.assertEqual(resp.status_code, 200)   
    
class TestLogoutView(TestCase):
  def test_get(self):
    resp = self.client.get('/logout/', {})
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="logged_out.html")
    self.assertEqual(resp.status_code, 200)    

class TestAllAssetsView(TestCase):
  def test_get(self):
    resp = self.client.get('/assets/', {})
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="all_assets.html")
    self.assertEqual(resp.status_code, 200)

class TestRegisterView(TestCase):
  def test_get(self):
    resp = self.client.get('/register/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="register.html")
    self.assertEqual(resp.status_code, 200)
    
  def test_post(self):
    resp = self.client.post('/register/', data={'username' : 'abacaba', 'email':'abacaba@gmail.com', 'password1':'Axksd32x', 'password2':'Axksd32x'}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="login.html")
    self.assertRedirects(response=resp, expected_url='/login/')

class TestLoginView(TestCase):
  def test_get(self):
    resp = self.client.get('/login/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="login.html")
    self.assertEqual(resp.status_code, 200)
  
  def test_post(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    resp = self.client.post('/login/', data={'username' : 'test', 'password':'test'}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="profile.html")
    self.assertRedirects(response=resp, expected_url='/profile/')
    self.assertEqual(resp.status_code, 200)
    u.delete()


class TestEditUserView(TestCase):
  def test_get_failure(self):
    with self.assertRaises(AttributeError):
      self.client.get('/profile/edit/')
    
  def test_get_success(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.get('/profile/edit/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="edit_user.html")
    self.assertEqual(resp.status_code, 200)
    self.client.logout()
    u.delete()
  
  def test_post(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.post('/profile/edit/', {'email' : "test@test.com"}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="profile.html")
    self.assertRedirects(resp, '/profile/')
    self.client.logout()
    u.delete()


class ChangePasswordView(TestCase):
  def test_get(self):
    resp = self.client.get('/profile/change_password/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="change_password.html")
  
  def test_post(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.post('/profile/change_password/', {'old_password':'test', 'new_password1' : "Aksaodkas241", 'new_password2' : "Aksaodkas241"}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="login.html")
    self.assertRedirects(resp, '/login/')
    self.client.logout()
    u.delete()

class TestAssetsView(TestCase):
  def test_get_failure(self):
    with self.assertRaises(ObjectDoesNotExist):
      resp = self.client.get('/profile/assets/')

  def test_get_success(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.get('/profile/assets/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="assets.html")
    self.assertEqual(resp.status_code, 200)
    self.client.logout()
    u.delete()
    
class TestAssetAddView(TestCase):
  def test_get(self):
    resp = self.client.get('/profile/assets/add')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="asset_add.html")
    self.assertEqual(resp.status_code, 200)

  def test_post(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.post('/profile/assets/add', {'ticker':'B3SA3', 'stop_loss_price':0.0, 'stop_limit_price':1.1}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="assets.html")
    self.assertRedirects(resp, '/profile/assets/')
    self.client.logout()
    u.delete()

class TestAssetRemoveView(TestCase):
  def test_get_failure(self):
    with self.assertRaises(ObjectDoesNotExist):
      resp = self.client.get('/profile/assets/remove')
  def test_get_success(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    self.client.login(username='test',password='test')
    resp = self.client.get('/profile/assets/remove')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="asset_remove.html")
    self.assertEqual(resp.status_code, 200)
  
  def test_post(self):
    u = User.objects.create(username="test")
    u.set_password('test')
    u.save()
    t = Asset.objects.create(ticker="B3SA3", user=u, stop_loss_price=0.0, stop_limit_price=1.1)
    t.save()
    self.client.login(username='test',password='test')
    resp = self.client.post('/profile/assets/remove', {'asset':t.id}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="assets.html")
    self.assertRedirects(resp, '/profile/assets/')
    self.client.logout()
    u.delete()

class TestSomeAssetView(TestCase):
  def test_get(self):
    resp = self.client.get('/assets/B3SA3/')
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="some_asset.html")
    self.assertEqual(resp.status_code, 200)
  
  def test_post(self):
    resp = self.client.post('/assets/B3SA3/', {'period': '5d'}, follow=True)
    self.assertTemplateUsed(response=resp, template_name="base.html")
    self.assertTemplateUsed(response=resp, template_name="some_asset.html")
    self.assertEqual(resp.status_code, 200)

class TestUserCreationForm(TestCase):
  def test_email_field_label(self):
    form = UserCreationForm()
    self.assertTrue(form.fields['email'].label == 'Email')
    
  def test_valid_user(self):
    form = UserCreationForm(data={
      'username':"test",
      'email':"test@test.com",
      'password1':"Akaskdjf21", 
      'password2':"Akaskdjf21"
    })
    self.assertTrue(form.is_valid())
    u = form.save()
    self.assertTrue(User.objects.filter(username="test").exists())
    u.delete()
    self.assertFalse(User.objects.filter(username="test").exists())
  
  def test_invalid_user(self):
    form = UserCreationForm(data={
      'username':"test",
      'email':"haha",
      'password1':"Akaskdjf21", 
      'password2':"Akaskdjf21"
    })
    self.assertFalse(form.is_valid())
    self.assertFalse(User.objects.filter(username="test").exists())
    
class TestEditUserForm(TestCase):    
  def test_field_labels(self):
    form = EditUserForm()
    self.assertTrue(form.fields['email'].label == 'Email')
    self.assertTrue(form.fields['first_name'].label == "First Name")
    self.assertTrue(form.fields['last_name'].label == "Last Name")  
    
  def test_valid_change(self):
    u = User.objects.create(username="test")
    form = EditUserForm(
      data={
        'email':"test@test.com",
        'first_name':"Test1", 
        'last_name':"Test2"
      },
      instance = u
    )
    self.assertTrue(form.is_valid())
    u = form.save()
    self.assertTrue(User.objects.filter(username="test").exists())
    self.assertEqual(u.email, "test@test.com")
    self.assertEqual(u.first_name, "Test1")
    self.assertEqual(u.last_name, "Test2")
    u.delete()
    self.assertFalse(User.objects.filter(username="test").exists())
  
  def test_invalid_change(self):
    u = User.objects.create(username="test")
    form = UserCreationForm(data={'email':"test"}, instance = u)
    self.assertFalse(form.is_valid())
    self.assertNotEqual(u.email, "test")
  def test_invalid_instance(self):
    form = UserCreationForm(data={
      'email':"test@test.com",
      'first_name':"Test1", 
      'last_name':"Test2"
    })
    self.assertFalse(form.is_valid())
    with self.assertRaises(ValueError):
      form.save()
    self.assertFalse(User.objects.filter(email="test@test.com").exists())
    
class TestTickerField(TestCase):
  def test_invalid_ticker(self):
    ticker = TickerField()
    with self.assertRaises(ValidationError):
      ticker.clean("TEST")
  
  def test_valid_ticker(self):
    ticker = TickerField()
    self.assertEqual(ticker.clean("B3SA3"), "B3SA3")

class TestTrackAssetForm(TestCase):
  def test_field_labels(self):
    form = TrackAssetForm()
    self.assertTrue(form.fields['ticker'].label == 'Ticker Symbol')
    self.assertTrue(form.fields['stop_loss_price'].label == "Stop Loss Price")
    self.assertTrue(form.fields['stop_limit_price'].label == "Stop Limit Price")
    
  def test_valid_asset(self):
    u = User.objects.create(username="testa")
    u.save()
    form = TrackAssetForm({
      'ticker': 'B3SA3',
      'stop_loss_price': 0.0,
      'stop_limit_price': 0.0,
      'user' : u
    })
    self.assertTrue(form.is_valid())
    form.save(id = u.id)
    self.assertTrue(Asset.objects.filter(user = u).exists())
    u.delete()
  
  def test_invalid_asset_limits(self):
    u = User.objects.create(username="testa")
    form = TrackAssetForm({
      'ticker': 'B3SA3',
      'stop_loss_price': 0.1,
      'stop_limit_price': 0.0,
      'user' : u
    })
    self.assertFalse(form.is_valid())
    with self.assertRaises(ValidationError):
      form.clean()    
    with self.assertRaises(ValidationError):
      form.save(id = u.id)  
  
  def test_invalid_asset_ticker(self):
    u = User.objects.create(username="test")
    form = TrackAssetForm({
      'ticker': 'TEST',
      'stop_loss_price': 0.0,
      'stop_limit_price': 0.0,
      'user' : u
    })
    self.assertFalse(form.is_valid())
    
class TestRemoveTrackedAssetForm(TestCase):
  def test_inexistent_user(self):
    with self.assertRaises(ObjectDoesNotExist):
      form = RemoveTrackedAssetForm(data={}, id = 0)
  
  def test_inexistent_asset(self):
    u = User.objects.create(username="test")
    a = Asset(ticker="a", user=u)
    with self.assertRaises(KeyError):
      form = RemoveTrackedAssetForm(data={'asset' : a}, id = u.id)
      self.assertFalse(form.is_valid())
      form.delete()
  
  def test_valid_removal(self):
    u = User.objects.create(username="test")
    a = Asset.objects.create(ticker="a", user = u)
    self.assertTrue(Asset.objects.filter(user = u).exists())
    form = RemoveTrackedAssetForm(data={'asset' : a}, id = u.id)
    self.assertTrue(form.is_valid())
    form.delete()
    self.assertFalse(Asset.objects.filter(user = u).exists())
    
class TestGraphPeriodForm(TestCase):
  def test_valid_choice(self):
    form = GraphPeriodForm(data={'period':'1d'})
    self.assertTrue(form.is_valid())
  
  def test_invalid_choice(self):
    form = GraphPeriodForm(data={'period':'1dd'})
    self.assertFalse(form.is_valid())
    
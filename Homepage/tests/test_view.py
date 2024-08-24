import pytest
from .factories import userFactory

@pytest.fixture
def logged_user(client):
    user = userFactory()
    client.login(username=user.username, password="password")
    return user    
"""test to check correct content in homepage template and it is rendered"""
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Today is " in response.content

"""test to ensure correct signup template is rendered"""
def test_signup(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert "signup.html" in response.template_name

"""
test to check the user is correctly redirected to notes_list.html while visiting signup again
"""
@pytest.mark.django_db
def test_signup_authenticated(client,logged_user):
    response = client.get("/signup", follow=True)

    assert response.status_code == 200
    assert "notes_list.html" in response.template_name


"""
test for the login view and page redirected to after login
"""
@pytest.mark.django_db
def test_login_authenticated(client,logged_user):
    response = client.get("/login", follow=True)
    assert response.status_code == 200
    assert "notes_list.html" in response.template_name

@pytest.mark.django_db
def test_signup_and_profile_page_being_created(client,logged_user):
    response = client.get("/signup", follow=True)
    assert response.status_code == 200
    assert logged_user.profile.user == logged_user
    response = client.get("/profile", follow=True)
    assert logged_user.username in str(response.content)
import pytest
from Homepage.tests.factories import userFactory , noteFactory

@pytest.fixture
def logged_user(client):
    user = userFactory()
    client.login(username=user.username, password="password")
    return user  



"""updated test_cases to show blogs of all users"""
@pytest.mark.django_db
def test_notes_listview_return_blogs_of_all_user(client,logged_user):
    note1 = noteFactory(user=logged_user)
    note2 = noteFactory()

    response = client.get("/notes")

    assert 200 == response.status_code
    assert note1.title in str(response.content) and note2.title in str(response.content)

"""to be made specific for each user profile to check blogs of only that user"""
# @pytest.mark.django_db
# def test_notes_listview_return_notes_of_only_logged_user(client,logged_user):
#     note1 = noteFactory(user=logged_user)
#     note2 = noteFactory()

#     response = client.get("/notes")

#     assert 200 == response.status_code
#     assert note1.title in str(response.content)

"""test to show only the details of a blog and not the delete and update buttons"""
@pytest.mark.django_db
def test_notes_detail_return_details_of_the_note(client,logged_user):
    note1 = noteFactory()
    note2 = noteFactory()
    response = client.get(f"/notes/{note1.id}")
    content = str(response.content)
    assert 200 == response.status_code
    assert note1.title in content and note2.title not in content
    assert 'class="btn btn-danger"' not in response.content.decode()
        
@pytest.mark.django_db
def test_notes_detail_return_details_of_the_note(client,logged_user):
    note1 = noteFactory(user=logged_user)
    note2 = noteFactory(user=logged_user)
    response = client.get(f"/notes/{note1.id}")
    content = str(response.content)
    assert 200 == response.status_code
    assert note1.title in content and note2.title not in content



@pytest.mark.django_db
def test_notes_createview_creates_new_note(client,logged_user):
    note = noteFactory()

    response = client.post(path="/notes/create",data = {"title":note.title,"text":note.text},follow=True)

    assert 200 == response.status_code
    assert 1==logged_user.notes.count()
    assert 'notes_list.html' in response.template_name




"""
Tests the update functionality of a note by checking if the note's text is updated correctly.

Parameters:
client (object): The test client.
logged_user (object): The user who is currently logged in.

Returns:
None
"""
@pytest.mark.django_db
def test_notes_updateview_updates_note(client,logged_user):
    note = noteFactory(user=logged_user)
    
    response = client.get(f"/notes/{note.id}")
    assert "test_check" not in str(response.content)
    test_text = note.text+" test_check"
    
    response = client.post(path=f"/notes/{note.id}/edit",data = {"title":note.title,"text":test_text},follow=True)
    assert 200 == response.status_code
    assert 1==logged_user.notes.count()
    assert 'notes_list.html' in response.template_name

    response = client.get(f"/notes/{note.id}")
    assert "test_check" in str(response.content)






@pytest.mark.django_db
def test_notes_updateview_updates_note_only_by_original_author(client, logged_user):
    # Create two users: user1 (original author) and user2 (another user)
    user1 = userFactory()
    user2 = userFactory()
    
    # Create a note by user1
    note = noteFactory(user=user1)
    
    # Log in as user1 (the original author)
    client.login(username=user1.username, password="password")
    
    # Ensure the note does not contain the test string before the update
    response = client.get(f"/notes/{note.id}")
    assert "test_check" not in str(response.content)
    
    # Update the note's text by adding "test_check"
    test_text = note.text + " test_check"
    response = client.post(
        path=f"/notes/{note.id}/edit", 
        data={"title": note.title, "text": test_text}, 
        follow=True
    )
    
    # Assert that the update is successful
    assert response.status_code == 200
    assert user1.notes.count() == 1  # Ensure user1 still owns one note
    assert 'notes_list.html' in response.template_name
    
    # Verify that the updated text is in the note content
    response = client.get(f"/notes/{note.id}")
    assert "test_check" in str(response.content)

    # Log out user1 and log in as user2
    client.logout()
    client.login(username=user2.username, password="password")
    
    # Try to update the note as user2 (should not be allowed)
    response = client.post(
        path=f"/notes/{note.id}/edit", 
        data={"title": note.title, "text": "unauthorized update attempt"}, 
        follow=True
    )
    
    # Ensure that user2 gets a 403 Forbidden response or appropriate handling
    assert response.status_code == 403

    # Ensure user2 still has no notes
    
    # Ensure that the note content remains unchanged after user2's failed attempt
    response = client.get(f"/notes/{note.id}")







@pytest.mark.django_db
def test_notes_delete_view(client,logged_user):
    note = noteFactory(user=logged_user)
    assert 1==logged_user.notes.count()
    response = client.post(path=f"/notes/{note.id}/delete",follow=True)

    assert 200 == response.status_code
    assert 'notes_list.html' in response.template_name
    assert 0==logged_user.notes.count()



@pytest.mark.django_db
def test_notes_delete_view_only_by_original_author(client,logged_user):
    # Create two users: user1 (original author) and user2 (another user)
    user1 = userFactory()
    user2 = userFactory()
    note = noteFactory(user=user1)
    client.login(username=user2.username, password="password")
    response = client.post(path=f"/notes/{note.id}/delete",follow=True)
    assert 403 == response.status_code
    assert 1==user1.notes.count()
    #assert 'Note not Found' in str(response.content)

import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


# 1. Проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_first_course(client, course_factory,):
    # Arrange
    course = course_factory(name='Python',)

    # Act
    response = client.get(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == 200
    assert response.data['name'] == 'Python'


# 2. Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses_list(client, course_factory,):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    response = client.get(f'/api/v1/courses/')
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == len(courses)

# 3. Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_course_id(client, course_factory,):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    # Act
    response = client.get(f'/api/v1/courses/?id={course_id}')
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == course_id

# 4. Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_courses_name(client, course_factory,):
    # Arrange
    courses = course_factory(_quantity=10)
    course_name = courses[0].name
    # Act
    response = client.get(f'/api/v1/courses/?name={course_name}')
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['name'] == course_name

# Тест успешного создания курса
@pytest.mark.django_db
def test_create_course_post(client,):
    # Arrange
    # Act
    response = client.post('/api/v1/courses/',data={'name': 'test'})
    # Assert
    assert response.status_code == 201

# 6. Тест успешного обновления курса
@pytest.mark.django_db
def test_update_course_put(client, course_factory,):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    # Act
    response = client.put(f'/api/v1/courses/{course_id}/',data={'name': 'test'})
    # Assert
    assert response.status_code == 200
    courses[0].refresh_from_db()
    assert courses[0].name == 'test'

# 7. Тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course_delete(client, course_factory,):
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    response = client.delete(f'/api/v1/courses/{course_id}/')

    assert response.status_code == 204

    response = client.get(f'/api/v1/courses/')
    response_json = response.json()
    check = [courses['id'] for courses in response_json]

    assert course_id not in check
    assert len(check) == 9














# def test_example():
#     assert False, "Just test example"

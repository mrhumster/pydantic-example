from datetime import datetime, date

from pydantic import BaseModel, ValidationError, field_validator


class Post(BaseModel):
    id: int
    title: str
    text: str
    is_published: bool
    tags: list[str] = []
    published_at: datetime | None = None

    @field_validator("published_at")
    def check_date_of_birth(self, value):
        # Преобразуем строку с датой в объект date
        date_of_birth = date.fromisoformat(value)
        today = date.today()
        if date_of_birth >= today:
            raise ValueError("Дата должна быть в прошлом")
        return value

    @field_validator("text")
    def check_text_not_empty(self, value, values):
        if not value:
            raise ValueError("Текст поста не может быть пустым")
        return value

    @field_validator("tags")
    def check_tags_if_published(self, value, values):
        is_published = values.get("is_published")
        if is_published and not value:
            raise ValueError("Если пост опубликован, необходимо указать хотя бы один тег")
        return value


if __name__ == '__main__':
    input_data = {
        'id': '1',
        'title': 'Python decorators',
        'text': 'Python decorators text',
        'is_published': True,
        'published_at': '2024-06-01 12:22',
        'tags': ['python', 'js', '3'],
        'another_field': 'Test data',
    }
    try:
        post = Post(**input_data)
        print(post.id, type(post.id))
        print(post.published_at, repr(post.published_at))
        print(post.model_dump())
        print(post.model_dump_json())
    except ValidationError as e:
        print(e.json())

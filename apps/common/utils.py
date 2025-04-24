from django.utils.text import slugify


def generate_unique_slug(model, name, field_name='slug'):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    existing_slugs = set(model.objects.values_list(field_name, flat=True))

    while slug in existing_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
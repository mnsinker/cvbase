from __future__ import annotations

from products.cv.entities.profile import Profile


def parse_profile(
    content: str,
) -> Profile:
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    name = ""
    phone = ""
    email = ""
    location = ""
    desired_position = ""

    for line in lines:
        if line.startswith("Phone:"):
            phone = line[len("Phone:"):].strip()
        elif line.startswith("Email:"):
            email = line[len("Email:"):].strip()
        elif line.startswith("Location:"):
            location = line[len("Location:"):].strip()
        elif line.startswith("Desired Position:"):
            desired_position = line[len("Desired Position:"):].strip()
        elif line.startswith("#"):
            continue
        elif not phone and not email and not location and not desired_position:
            name = line

    return Profile(
        name=name,
        phone=phone,
        email=email,
        location=location,
        desired_position=desired_position,
    )

#!/bin/bash

echo "BUILD START"

# Install pip if missing
python3.9 -m ensurepip --default-pip

# Upgrade pip
python3.9 -m pip install --upgrade pip

# Install dependencies from requirements.txt
python3.9 -m pip install -r requirements.txt

# Ensure the staticfiles_build directory exists
mkdir -p staticfiles

# Collect static files (ensure it's pointing to the correct directory)
python3.9 manage.py collectstatic --noinput --clear

# Run migrations
python3.9 manage.py migrate

# Create superuser (non-interactive)
python3.9 manage.py shell <<EOF
from django.contrib.auth.models import User;
User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword');
EOF

# Debug: List files in staticfiles_build
ls -lah staticfiles

echo "BUILD END"

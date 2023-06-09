#!/usr/bin/python3
"""Rent post form module"""

from web_dynamic_admin.views import app_views
from flask import jsonify, render_template
from flask_login import login_required
import uuid


@app_views.route('/rent-post', methods=['GET'], strict_slashes=False)
@login_required
def rent_post():
    """Returns the rent post form"""
    cache_id = uuid.uuid4()
    return render_template('rent_post_form.html', cache_id=cache_id)

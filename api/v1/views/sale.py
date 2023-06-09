#!/usr/bin/python3
"""API sale module"""

from api.v1.views import app_views
from api.v1.app import requires_auth
from datetime import datetime
from flask import jsonify, make_response, request, abort
from flasgger.utils import swag_from
from models import storage
from models.sale import Sale
import os
import shutil
import pytz


@app_views.route('/sale', methods=['GET'], strict_slashes=False)
@swag_from('documentation/sale/get_sale.yml', methods=['GET'])
def get_sale_props_api():
    """Retrieves all properties for sale"""
    sale_props = storage.all(Sale).values()
    list_sale = []
    for prop in sale_props:
        list_sale.append(prop.to_dict())
    
    list_sale = sorted(list_sale, key=lambda x: datetime.fromisoformat(
                       x['updated_at']), reverse=True)

    return jsonify(list_sale)


@app_views.route('/sale/<sale_id>', methods=['GET'], strict_slashes=False)
@requires_auth
@swag_from('documentation/sale/get_id_sale.yml', methods=['GET'])
def get_sale_prop_api(sale_id):
    """Retrieves a single property for sale"""
    sale_prop = storage.get(Sale, sale_id)
    if not sale_prop:
        abort(404)

    return jsonify(sale_prop.to_dict())


@app_views.route('/sale', methods=['POST'], strict_slashes=False)
@requires_auth
@swag_from('documentation/sale/post_sale.yml', methods=['POST'])
def post_sale_api():
    """Creates a new sale property in the db"""
    title = request.form.get('title')
    price = request.form.get('price')
    location = request.form.get('location')
    description = request.form.get('description')

    if not price or not location or not title:
        abort(400, description="price, location and title cannot be null")

    sale_prop = Sale(description=description, location=location, price=price, title=title)

    # Handle the saving of media files
    prop_id = sale_prop.id

    # Access uploaded images separately
    images = request.files.getlist('images')
    if images and any(images):
        for image in images:
            base_dir = '/home/vagrant/alx/skyspringhomes/web_dynamic/static/media_storage/sale/images/'
            os.makedirs(base_dir, exist_ok=True)

            prop_dir = os.path.join(base_dir, prop_id)
            os.makedirs(prop_dir, exist_ok=True)

            filename = image.filename
            image.save(os.path.join(prop_dir, filename))
    else:
        abort(400, description="upload at least one image for the property")

    # Access uploaded videos separately
    # if 'videos' in request.files:
    #     videos = request.files.getlist('videos')
    #     for video in videos:
    #         base_dir = '/home/vagrant/alx/skyspringhomes/web_dynamic/static/media_storage/sale/videos/'
    #         os.makedirs(base_dir, exist_ok=True)

    #         prop_dir = os.path.join(base_dir, prop_id)
    #         os.makedirs(prop_dir, exist_ok=True)

    #         filename = video.filename
    #         video.save(os.path.join(prop_dir, filename))

    sale_prop.save()
    print("sale property saved successfully")
    return make_response(jsonify(sale_prop.to_dict()), 200)


@app_views.route('/sale/<sale_id>', methods=['PUT'], strict_slashes=False)
@requires_auth
@swag_from('documentation/sale/put_sale.yml', methods=['PUT'])
def put_sale_api(sale_id):
    """Updates a sale property in the db"""

    sale_prop = storage.get(Sale, sale_id)
    if not sale_prop:
        abort(404)

    # Handle update for db information
    ignore = ['id', 'created_at']

    data = request.form
    for key, value in data.items():
        if key not in ignore:
            setattr(sale_prop, key, value)
    setattr(sale_prop, 'updated_at', datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos')))

    # Handle update for images/videos
    images = request.files.getlist('images')

    if images and any(images):
        image_path = sale_prop.image_path
        # Delete the existing dir
        if os.path.exists('/home/vagrant/alx/skyspringhomes/web_dynamic' + image_path):
            shutil.rmtree('/home/vagrant/alx/skyspringhomes/web_dynamic' + image_path)
        else:
            pass
        # Create a new dir with updated images
        for image in images:
            base_dir = '/home/vagrant/alx/skyspringhomes/web_dynamic/static/media_storage/sale/images/'
            os.makedirs(base_dir, exist_ok=True)

            prop_dir = os.path.join(base_dir, sale_id)
            os.makedirs(prop_dir, exist_ok=True)

            filename = image.filename
            image.save(os.path.join(prop_dir, filename))
    else:
        pass


    # if 'videos' in request.files:
    #     video_path = sale_prop.video_path
    #     # Delete the existing dir
    #     if os.path.exists('/home/vagrant/alx/skyspringhomes/web_dynamic' + video_path):
    #         shutil.rmtree('/home/vagrant/alx/skyspringhomes/web_dynamic' + video_path)
    #     else:
    #         pass
    #     # Create a new dir with updated videos
    #     videos = request.files.getlist('videos')
    #     for video in videos:
    #         base_dir = '/home/vagrant/alx/skyspringhomes/web_dynamic/static/media_storage/sale/videos/'
    #         os.makedirs(base_dir, exist_ok=True)

    #         prop_dir = os.path.join(base_dir, sale_id)
    #         os.makedirs(prop_dir, exist_ok=True)

    #         filename = video.filename
    #         video.save(os.path.join(prop_dir, filename))

    storage.save()
    return make_response(jsonify(sale_prop.to_dict()), 200)


@app_views.route('/sale/<sale_id>', methods=['DELETE'], strict_slashes=False)
@requires_auth
@swag_from('documentation/sale/delete_sale.yml', methods=['DELETE'])
def delete_sale_api(sale_id):
    """Deletes a sale property from the db"""
    
    sale_prop = storage.get(Sale, sale_id)
    if not sale_prop:
        abort(404)

    # Handle deletion of image/videos from file system
    image_path = sale_prop.image_path
    # video_path = sale_prop.video_path

    
    if os.path.exists('/home/vagrant/alx/skyspringhomes/web_dynamic' + image_path):
        shutil.rmtree('/home/vagrant/alx/skyspringhomes/web_dynamic' + image_path)
    else:
        pass

    # if os.path.exists('/home/vagrant/alx/skyspringhomes/web_dynamic' + video_path):
        # shutil.rmtree('/home/vagrant/alx/skyspringhomes/web_dynamic' + video_path)
    # else:
    #     pass

    # Handle deletion of object from the db
    storage.delete(sale_prop)
    storage.save()

    return make_response(jsonify({}), 200)

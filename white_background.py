import requests
import os

def remove_background(enhanced_image_path):
    final_image_dir = 'static/images'

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(enhanced_image_path, 'rb')},
        data={'size': 'auto', 'bg_color': 'white'},
        headers={'X-Api-Key': 'kbddzWHoV9YZaa4g3zZY8RnS'},  # Insert your API key here
    )

    if response.status_code == requests.codes.ok:
        if not os.path.exists(final_image_dir):
            os.makedirs(final_image_dir)

        final_image_filename = os.path.basename(enhanced_image_path)
        final_image_path = os.path.join(final_image_dir, final_image_filename)
        with open(final_image_path, 'wb') as out:
            out.write(response.content)
        return final_image_path
    else:
        return None

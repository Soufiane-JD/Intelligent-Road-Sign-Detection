import firebase_admin
from firebase_admin import credentials, firestore, storage


class DatabaseManager:
    def __init__(self, credential_path, bucket_name):
        # Initialize Firebase Admin SDK
        self.cred = credentials.Certificate(credential_path)
        self.app = firebase_admin.initialize_app(self.cred)
        # firebase_app = firebase_admin.initialize_app(self.cred, {
        #     'storageBucket': bucket_name
        # })

        # Get a reference to the Firestore service
        self.db = firestore.client()
        self.bucket_name = bucket_name

    # Upload an image to Firebase Storage and get the public URL
    # image_url = upload_image('local/path/to/stop_sign.jpg', 'stop')
    def upload_image(self, file_path, blob_name):
        try:
            # Ensure the bucket name matches with your Firebase Storage bucket
            bucket = storage.bucket(self.bucket_name, app=self.app)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            blob.make_public()  # Make the blob publicly viewable
            print(f"Image uploaded successfully: {blob.public_url}")
            return blob.public_url
        except Exception as e:
            print(f"Failed to upload image: {e}")
            return None

    # Function to add a sign to the Firestore
    # Exemple: add_sign('stop_sign', 'A sign to make vehicles stop.', 'path/to/stop_sign.jpg')
    def add_sign(self, sign_id, description, image_path):
        try:
            doc_ref = self.db.collection('signs').document(sign_id)
            doc_ref.set({
                'description': description,
                'image_path': image_path
            })
            print(f"Sign {sign_id} added successfully.")
        except Exception as e:
            print(f"Failed to add sign {sign_id}: {e}")

    # Function to get a sign by its ID
    # get_sign('stop_sign')
    def get_sign(self, sign_id):
        try:
            doc_ref = self.db.collection('signs').document(sign_id)
            sign = doc_ref.get()
            if sign.exists:
                print(f"Sign {sign_id} retrieved successfully.")
                return sign.to_dict()
            else:
                print(f"No sign found with ID: {sign_id}")
                return None
        except Exception as e:
            print(f"Error retrieving sign {sign_id}: {e}")
            return None

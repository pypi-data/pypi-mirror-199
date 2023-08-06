import io
import pickle

import boto3
import h5py


class S3Client(object):
    def __init__(self, BUCKET_NAME: str, ACCESSKEY=False, SECRETKEY=False):
        self.BUCKET_NAME = BUCKET_NAME
        
        self.s3 = boto3.client('s3', 
                               aws_access_key_id=ACCESSKEY,
                               aws_secret_access_key=SECRETKEY)
        
    
    def get_latest_file_key(self, storage_path: str) -> str : 
        contents_list = self.s3.list_objects(Bucket=self.BUCKET_NAME, Prefix=storage_path)['Contents']
        storage_path = [i['Key'] for i in contents_list][-1]
        
        return '/'.join(storage_path.split('/'))
    
    
    def get_latest_folder_key(self, storage_path: str) -> str:
        contents_list = self.s3.list_objects(Bucket=self.BUCKET_NAME, Prefix=storage_path)['Contents']
        storage_path = [i['Key'] for i in contents_list][-1]
        
        return '/'.join(storage_path.split('/')[:-1])
    
    
    def get_pkl_file(self, key: str) -> object :
        with io.BytesIO() as byte_io:
            self.s3.download_fileobj(self.BUCKET_NAME, key, byte_io)
            byte_io.seek(0)
            
            return pickle.load(byte_io)
        
        
    def get_h5_file(self, model_key: str) -> object :
        s3 = boto3.client('s3',
                          aws_access_key_id = self.ACCESSKEY,
                          aws_secret_access_key = self.SECRETKEY,
                          )
        with io.BytesIO() as model_io:
            s3.download_fileobj(self.BUCKET_NAME, model_key, model_io)
            model_io.seek(0)
            with h5py.File(model_io, 'r') as f:
                loaded_model = tf.keras.models.load_model(f)
                
        return loaded_model
    
    
    def get_byte_file(self, key: str) -> object :
      
        s3_object = s3.get_object(Bucket=self.BUCKET_NAME, Key=key)['Body']
        byte_data = s3_object.read()
        data = byte_data.decode('utf-8')

        return data
    
    def upload_pkl_file(self, save_key: str, data: object):
        with io.BytesIO() as byte_io:
            pickle.dump(data, byte_io)
            byte_io.seek(0)
            
            return s3.upload_fileobj(byte_io, self.BUCKET_NAME, save_key)
        
        
    def upload_h5_file(self, save_key: str, data: object):
        with io.BytesIO() as data_io:
            with h5py.File(data_io, 'w') as f:
                data.save(f)
            data_io.seek(0)
            
            return s3.upload_fileobj(data_io, self.BUCKET_NAME, save_key)
    
    def upload_byte_file(self, save_key: str, data: str): # txt, csv, doc ..
      
        byte_io = io.BytesIO()
        byte_io.write(bytes(data, 'utf-8'))
        
        return s3.put_object(Bucket = self.BUCKET_NAME, Body = byte_io.getvalue(), Key = save_key) 

    

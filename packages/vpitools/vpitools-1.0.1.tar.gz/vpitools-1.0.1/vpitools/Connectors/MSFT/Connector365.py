#Function to create authentication for Sharepoint 365 of Microsoft
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import os
#---------------------------------------------------------------------------------------------------------
class SharepointData:
    def __init__(self, site_url, client_id, client_secret) -> None:
        self.site_url = site_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.ctx = ClientContext(self.site_url).with_credentials(ClientCredential(self.client_id, self.client_secret))
        
    def get_subfolders(self, root_url):
        #Get Folder from server
        folders = self.ctx.web.get_folder_by_server_relative_url(root_url).folders
        #Get Sub-folders
        self.ctx.load(folders).execute_query()
        return folders
    
    def get_files(self, root_url):
        #Get Folder from server
        files = self.ctx.web.get_folder_by_server_relative_url(root_url).files
        #Get files in the current folder
        self.ctx.load(files).execute_query()
        return files
    
    def get_subfolders_url(self, root_url):
        folder_list=[]
        folders = self.ctx.web.get_folder_by_server_relative_url(root_url).folders
        self.ctx.load(folders).execute_query()
        for folder in folders:
            folder_list.append(folder.properties['ServerRelativeUrl'] + '/')
        return folder_list
    
    def get_files_url(self, root_url):
        files_list=[]
        files = self.ctx.web.get_folder_by_server_relative_url(root_url).files
        self.ctx.load(files).execute_query()
        for file in files:
            files_list.append(file.properties['ServerRelativeUrl'])
        return files_list
    
    def download(self, file_url, local_folder_path):
        file_name = file_url.split('/')[-1]
        # file_url is the relative url of the file in sharepoint
        file_path = local_folder_path + file_name
        with open(file_path, "wb") as local_file:
            file = self.ctx.web.get_file_by_server_relative_url(file_url)
            file.download(local_file)
            self.ctx.execute_query()
        print(f"-----Downloaded: {file_name}-----")
        return file_path
    
    def upload(self, file_path, destn_url, remove:bool=False):
        file_name = file_path.split('/')[-1]
        #upload to sharepoint
        destn_folder = self.ctx.web.get_folder_by_server_relative_url(destn_url)
        with open(file_path, 'rb') as content_file:
            file_content = content_file.read()
            destn_folder.upload_file(file_name, file_content).execute_query()
            print(f'{file_name}: Uploaded!')
        if remove:
            os.remove(file_path); print(f'{file_name}: Uploaded & Removed local file!')
            
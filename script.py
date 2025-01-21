# import subprocess
# import requests
# from pathlib import Path
# import os
# import zipfile
#
# def create_db_dump(docker_container_name, user, password, db_name, dump_file):
#     command = [
#         'docker', 'exec', docker_container_name,
#         'mariadb-dump', f'--user={user}', f'--password={password}', db_name
#     ]
#
#     with open(dump_file, 'wb') as f:
#         subprocess.run(command, stdout=f)
#
# def zip_file(file_to_zip, zip_file_name):
#     with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         zipf.write(file_to_zip, arcname=Path(file_to_zip).name)
#
# def upload_backup(zip_file_name, api_url, backup_rule_id, password):
#     with open(zip_file_name, 'rb') as f:
#         mimetype = 'application/zip'
#         files = {'backup': (Path(zip_file_name).name, f, mimetype)}
#         data = {
#             'backupRuleId': backup_rule_id,
#             'password': password
#         }
#         response = requests.post(api_url, files=files, data=data)
#         return response
#
# def main():
#     docker_container_name = 'greeksnowresortsapi-mysql-1'
#     db_host = 'localhost'
#     db_user = 'root'
#     db_password = 'password'
#     db_name = 'laravel'
#     api_url = 'http://localhost:999/api/backups/push/f2279e84-7442-4074-8824-26dd3eff3b45'
#     backup_rule_id = 'd6a98cc8-f63b-46b4-a525-0322504ba457'
#     password = 'password'
#     dump_file = r'C:\Users\pants\Documents\dumps\backup.sql'
#     zip_file_name = r'C:\Users\pants\Documents\dumps\backup.zip'
#
#     try:
#         print("creating database dump...")
#         create_db_dump(docker_container_name, db_user, db_password, db_name, dump_file)
#         print(f"database dump created at {dump_file}")
#         zip_file(dump_file, zip_file_name)
#         print(f"dump file zipped at {zip_file_name}")
#
#         print("uploading backup to the APi")
#         response = upload_backup(zip_file_name, api_url, backup_rule_id, password)
#
#         if response.status_code == 200:
#             print("backup uploaded successfully!")
#         else:
#             print(f"failed to upload backup. status code: {response.status_code}, Response: {response.text}")
#
#     finally:
#         if Path(dump_file).exists():
#             os.remove(dump_file)
#             print(f"deleted  dump file {dump_file}")
#         if Path(zip_file_name).exists():
#             os.remove(zip_file_name)
#             print(f"deleted  zip file {zip_file_name}")
#
# if __name__ == "__main__":
#     main()

import subprocess
import requests
from pathlib import Path
import os
import zipfile


def create_db_dump(user, password, db_name, dump_file):
    command = [
        # 'mariadb-dump', f'--user={user}', f'--password={password}', db_name, '--single-transaction=false'
        'mysqldump', f'--user={user}', f'--password={password}', db_name, '--single-transaction=false'
    ]

    with open(dump_file, 'wb') as f:
        result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"error creating database dump: {result.stderr.decode()}")


def zip_file(file_to_zip, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_to_zip, arcname=Path(file_to_zip).name)


def upload_backup(zip_file_name, api_url, backup_rule_id, password):
    with open(zip_file_name, 'rb') as f:
        mimetype = 'application/zip'
        files = {'backup': (Path(zip_file_name).name, f, mimetype)}
        data = {
            'backupRuleId': backup_rule_id,
            'password': password
        }
        response = requests.post(api_url, files=files, data=data)
        return response


def main():
    db_user = 'root'
    db_password = 'password'
    db_name = 'magento'
    api_url = 'http://localhost:999/api/backups/push/f2279e84-7442-4074-8824-26dd3eff3b45'
    backup_rule_id = 'd6a98cc8-f63b-46b4-a525-0322504ba457'
    password = 'password'
    dump_file = '/tmp/backup.sql'
    zip_file_name = '/tmp/backup.zip'

    try:
        print("creating database dump...")
        create_db_dump( db_user, db_password, db_name, dump_file)
        print(f"database dump created at {dump_file}")

        print("compressing dump file...")
        zip_file(dump_file, zip_file_name)
        print(f"dump file zipped at {zip_file_name}")

        print("uploading backup to the API...")
        response = upload_backup(zip_file_name, api_url, backup_rule_id, password)

        if response.status_code == 200:
            print("backup uploaded successfully!")
        else:
            print(f"failed to upload backup. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if Path(dump_file).exists():
            os.remove(dump_file)
            print(f"deleted  dump file {dump_file}")
        if Path(zip_file_name).exists():
            os.remove(zip_file_name)
            print(f"deleted  zip file {zip_file_name}")


if __name__ == "__main__":
    main()
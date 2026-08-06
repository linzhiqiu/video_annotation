import labelbox as lb
from labelbox import Client
from uuid import uuid4
import datetime
import shutil


API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbTJmbnRwbngwNXFlMDcxejg4YnEzMjYyIiwib3JnYW5pemF0aW9uSWQiOiJjbTA3b2RubGEwZjR5MDd2YWJzc2g4ZXdkIiwiYXBpS2V5SWQiOiJjbTg1azczczUwaDZ1MDcxMWM5Zmtob2owIiwic2VjcmV0IjoiZTZmNTc0Zjc5MzdmYzU5ZDAwMGUwODVlYmVlYTY2ZTkiLCJpYXQiOjE3NDE3NjIxMjMsImV4cCI6MTc0NzgxMDEyM30.-8svjKnhqsiX3Go6S2oliYGciOaLBrPt_1-5fWrPJ5s"
project_id = 'cm85167um071b074o4os3f788'
target_path = './labelbox_test/test.ndjson'
client = Client(api_key=API_KEY)
project  = client.get_project(project_id)
defaults = {
    "attachments": False,
    "metadata_fields": False,
    "data_row_details": True,
    "project_details": True,
    "label_details": True,
    "performance_details": True,
    "interpolated_frames": False,
    "embeddings": False
}
export_task = project.export(
    params=defaults,
    filters={workflow_status: "Done"}
)



# dataset = client.create_dataset(name="test_video_set")
#
# video_data = [
#   {
#     "row_data": "https://lb-test-data.s3.us-west-1.amazonaws.com/video-samples/sample-video-1.mp4",
#     "global_key": "https://lb-test-data.s3.us-west-1.amazonaws.com/video-samples/sample-video-1.mp4",
#     "media_type": "VIDEO",
#   },
#   {
#     "row_data": "https://lb-test-data.s3.us-west-1.amazonaws.com/video-samples/sample-video-2.mp4",
#     "global_key": "https://lb-test-data.s3.us-west-1.amazonaws.com/video-samples/sample-video-2.mp4",
#     "media_type": "VIDEO",
#   }
# ]
#
# task = dataset.create_data_rows(video_data)
# task.wait_till_done()
# print(task.errors)

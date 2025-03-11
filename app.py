from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError
from typing import Dict
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/swagger-ui",  # Đổi URL mặc định Swagger từ /docs -> /swagger-ui
    redoc_url="/redoc-api",  # Đổi URL Redoc từ /redoc -> /redoc-api
)

# AWS S3 configuration
S3_BUCKET = "elearning-web"  # Thay bằng tên bucket của bạn
S3_REGION = "ap-southeast-1"  # Ví dụ: "ap-southeast-1"
AWS_ACCESS_KEY = ""  # Thay bằng Access Key của bạn
AWS_SECRET_KEY = ""  # Thay bằng Secret Key của bạn

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn (có thể thay bằng danh sách domain cụ thể)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả HTTP methods
    allow_headers=["*"],  # Cho phép tất cả headers
)


@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    API endpoint để upload video lên AWS S3
    """
    try:
        # # Kiểm tra loại file
        # if not file.content_type.startswith("video/"):
        #     raise HTTPException(status_code=400, detail="File không phải video!")

        # Gửi file lên S3
        file_key = f"uploads/{file.filename}"  # Đây sẽ là đường dẫn trong bucket
        s3.upload_fileobj(
            file.file,  # Nội dung file
            S3_BUCKET,  # Bucket đích
            file_key,  # Key trong bucket
            ExtraArgs={"ContentType": file.content_type}
        )

        # Tạo URL công khai đến file vừa upload
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"

        return {
            "message": "Video uploaded successfully",
            "url": file_url  # Trả về đường link công khai của video
        }

    except NoCredentialsError:
        # Lỗi không tìm thấy AWS Credentials
        raise HTTPException(status_code=500, detail="AWS credentials không hợp lệ hoặc không tìm thấy!")
    except Exception as e:
        # Bắt các lỗi khác
        raise HTTPException(status_code=500, detail=f"Lỗi trong quá trình upload: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)

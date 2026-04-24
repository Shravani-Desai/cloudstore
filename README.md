# CloudStore – Serverless File Manager

A serverless REST API for managing file uploads and downloads, built entirely on AWS using Lambda, S3, API Gateway, and DynamoDB. Deployed within the AWS Free Tier.

## Architecture

```
Client → API Gateway → Lambda Functions → S3 (file storage)
                                        → DynamoDB (metadata)
```

### AWS Services Used
- **AWS Lambda** – Three serverless functions handling upload, download, and listing
- **Amazon S3** – File storage with public access blocked; files accessed via presigned URLs
- **Amazon API Gateway** – REST API with three endpoints
- **Amazon DynamoDB** – Stores file metadata (name, size, timestamp, owner) with a GSI for owner-based queries
- **AWS IAM** – Least-privilege roles per Lambda function
- **Amazon CloudWatch** – Error rate and throttle alarms for each function

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Generate a presigned S3 URL for file upload and save metadata |
| GET | `/files` | List all files |
| GET | `/files?owner={owner}` | List files filtered by owner |
| GET | `/file/{file_id}` | Get a presigned download URL for a specific file |

## Project Structure

```
cloudstore/
├── template.yaml              # SAM infrastructure definition
├── samconfig.toml             # SAM deployment config
├── test_api.py                # End-to-end API test script
├── functions/
│   ├── upload_file/
│   │   └── handler.py         # Generates presigned PUT URL, saves metadata
│   ├── download_file/
│   │   └── handler.py         # Looks up metadata, returns presigned GET URL
│   └── list_files/
│       └── handler.py         # Queries DynamoDB by owner or scans all files
└── events/
    ├── upload.json            # Test event for upload function
    └── download_payload.json  # Test event for download function
```

## DynamoDB Schema

**Table:** `cloudstore-files`  
**Partition Key:** `file_id` (String)  
**GSI:** `owner-index` on `owner` field

| Attribute | Type | Description |
|-----------|------|-------------|
| file_id | String | UUID, primary key |
| filename | String | Original file name |
| size | Number | File size in bytes |
| owner | String | Owner identifier |
| timestamp | Number | Unix timestamp of upload |
| s3_key | String | S3 object key path |

## IAM Least-Privilege Policies

Each Lambda function has its own IAM role with only the permissions it needs:

| Function | Allowed Actions |
|----------|----------------|
| upload_file | `s3:PutObject`, `dynamodb:PutItem` |
| download_file | `s3:GetObject`, `dynamodb:GetItem` |
| list_files | `dynamodb:Scan`, `dynamodb:Query` |

## CloudWatch Alarms

Six alarms monitor the health of all three functions:

- `cloudstore-upload-errors` – triggers if errors ≥ 3 in 60 seconds
- `cloudstore-upload-throttles` – triggers if throttles ≥ 5 in 60 seconds
- `cloudstore-download-errors`
- `cloudstore-download-throttles`
- `cloudstore-list-errors`
- `cloudstore-list-throttles`

## Prerequisites

- Python 3.11+
- AWS CLI configured (`aws configure`)
- AWS SAM CLI

## Deployment

```bash
sam deploy --guided
```

Follow the prompts:
- Stack name: `cloudstore`
- Region: `us-east-1`
- Allow IAM role creation: `y`

On subsequent deploys:
```bash
sam deploy
```

## Testing

Install dependencies:
```bash
pip install requests
```

Run the test script:
```bash
python test_api.py
```

Expected output:
```
Starting CloudStore API tests...

--- Test 1: Upload file ---
Status: 200
File ID: <uuid>
Upload URL: https://...

--- Test 2: List all files ---
Status: 200
Total files: 4

--- Test 3: List files by owner ---
Status: 200
Files owned by shravani: 4

--- Test 4: Download file ---
Status: 200
Filename: demo.txt
Download URL: https://...

--- Test 5: File not found ---
Status: 404
Response: {'error': 'File not found'}

All tests complete!
```

## Free Tier

This project is designed to run entirely within the AWS Free Tier:

| Service | Free Tier Limit |
|---------|----------------|
| Lambda | 1M requests/month |
| API Gateway | 1M calls/month (12 months) |
| S3 | 5GB storage (12 months) |
| DynamoDB | 25GB + 25M requests/month (forever) |
| CloudWatch | 10 alarms (forever) |

## License

MIT

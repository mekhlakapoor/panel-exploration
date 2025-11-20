"""Tab 4: S3 connection using boto3"""

import os
import tempfile
from typing import Optional

import panel as pn
import param
import boto3
import httpx

class S3Explorer(pn.custom.PyComponent):
    """
    Explores S3 objects using boto3 with presigned URLs
    """
    bucket_name = param.String(default="")
    object_key = param.String(default="")
    
    def __init__(self, **params):
        super().__init__(**params)
        self.s3_client = boto3.client(
            "s3",
            region_name="us-west-2",
        )
        self._status_pane = pn.pane.Markdown("Ready to query S3...")
        self._preview_pane = pn.Column(sizing_mode="stretch_both")
        self._info_pane = pn.pane.JSON({}, depth=2, theme="light")
        
        # Watch params for changes
        self.param.watch(self._update_preview, ['bucket_name', 'object_key'])
    
    def _generate_presigned_url(self, bucket: str, key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a presigned URL for S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def _get_object_metadata(self, bucket: str, key: str) -> dict:
        """Get metadata for an S3 object"""
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            return {
                "Size": response.get("ContentLength", "Unknown"),
                "ContentType": response.get("ContentType", "Unknown"),
                "LastModified": str(response.get("LastModified", "Unknown")),
                "ETag": response.get("ETag", "Unknown"),
            }
        except Exception as e:
            return {"Error": str(e)}
    
    def _is_image(self, key: str) -> bool:
        """Check if object is an image"""
        return key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.tiff'))
    
    def _is_video(self, key: str) -> bool:
        """Check if object is a video"""
        return key.lower().endswith(('.mp4', '.avi', '.webm'))
    
    def _is_pdf(self, key: str) -> bool:
        """Check if object is a PDF"""
        return key.lower().endswith('.pdf')
    
    def _fetch_object_data(self, url: str) -> Optional[str]:
        """Fetch object data and save to temporary file"""
        try:
            with httpx.Client() as client:
                response = client.get(url, follow_redirects=True)
            
            if response.status_code == 200:
                # Get file extension from key
                ext = os.path.splitext(self.object_key)[1] or '.tmp'
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                    temp_file.write(response.content)
                    return temp_file.name
            else:
                print(f"Failed to fetch: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching object: {e}")
            return None
    
    def _update_preview(self, event):
        """Callback when parameters change"""
        if not self.bucket_name or not self.object_key:
            self._status_pane.object = "Enter bucket name and object key above..."
            self._preview_pane.clear()
            self._info_pane.object = {}
            return None
        
        try:
            self._status_pane.object = "Fetching S3 object..."
            metadata = self._get_object_metadata(self.bucket_name, self.object_key)
            self._info_pane.object = metadata
            
            if "Error" in metadata:
                self._status_pane.object = f"Error: {metadata['Error']}"
                self._preview_pane.clear()
                return None
            
            # Generate presigned URL (QC Portal pattern)
            url = self._generate_presigned_url(self.bucket_name, self.object_key)
            if not url:
                self._status_pane.object = "Error generating presigned URL"
                self._preview_pane.clear()
                return None
            
            self._preview_pane.clear()
            
            if self._is_video(self.object_key):
                self._preview_pane.append(
                    pn.pane.Video(url, sizing_mode="scale_width", max_width=1200, loop=False)
                )
                self._status_pane.object = "Video preview loaded"
            elif self._is_pdf(self.object_key):
                self._preview_pane.append(
                    pn.pane.PDF(url, sizing_mode="scale_width", max_width=1200, height=1000)
                )
                self._status_pane.object = "PDF preview loaded"
            elif self._is_image(self.object_key):
                self._preview_pane.append(
                    pn.pane.Image(url, sizing_mode="scale_width", max_width=1200)
                )
                self._status_pane.object = "Image preview loaded"
            else:
                self._preview_pane.append(
                    pn.pane.Markdown(f"[Download {self.object_key}]({url})")
                )
                self._status_pane.object = "File ready for download"
        
        except Exception as e:
            self._status_pane.object = f"Error: {str(e)}"
            self._preview_pane.clear()
            self._info_pane.object = {}
    
    def __panel__(self):
        return pn.Column(
            self._status_pane,
            pn.layout.Divider(),
            "### Object Metadata",
            self._info_pane,
            pn.layout.Divider(),
            "### Preview",
            self._preview_pane,
        )

def create_s3_tab():
    """Create the S3 connection tab"""
    s3_explorer = S3Explorer()
    
    bucket_input = pn.widgets.TextInput(
        name="Bucket Name",
        value="aind-open-data",
        placeholder="e.g., aind-open-data"
    )
    
    key_input = pn.widgets.TextInput(
        name="Object Key",
        placeholder="e.g., ecephys_625749_2022-08-03_15-15-06/ecephys_clipped.mp4"
    )
    
    fetch_button = pn.widgets.Button(name="Fetch Object", button_type="primary")
    
    def on_fetch(event):
        s3_explorer.bucket_name = bucket_input.value
        s3_explorer.object_key = key_input.value
    
    fetch_button.on_click(on_fetch)
    
    return pn.Column(
        "## S3 Connection",
        """
        This demonstrates connecting to S3 using boto3 with presigned URLs.
        """,
        pn.Row(
            pn.Column(
                "### S3 Object Selector",
                bucket_input,
                key_input,
                fetch_button,
                width=400
            ),
            pn.Column(
                "### Object Details & Preview",
                s3_explorer,
            )
        ),
    )
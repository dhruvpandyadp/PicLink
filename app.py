import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# Set page config
st.set_page_config(page_title="PicLink - Image Upload & Share", page_icon="🖼️", layout="wide")

# Title and description
st.title("🖼️ PicLink - Image Upload & Share")
st.markdown("Upload an image to preview it and get a shareable URL")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
    help="Upload an image to preview and share"
)

if uploaded_file is not None:
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📸 Image Preview")
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        # Show image details
        st.caption(f"**Filename:** {uploaded_file.name}")
        st.caption(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        st.caption(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
    
    with col2:
        st.subheader("🔗 Share Image")
        
        # Convert image to base64 for data URL
        buffered = BytesIO()
        image.save(buffered, format=image.format if image.format else "PNG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode()
        
        # Create data URL
        mime_type = uploaded_file.type
        data_url = f"data:{mime_type};base64,{img_base64}"
        
        # Display the URL in a text area
        st.text_area(
            "Image Data URL",
            value=data_url,
            height=150,
            help="This is a base64-encoded data URL that contains your image"
        )
        
        # Copy button
        if st.button("📋 Copy URL to Clipboard", use_container_width=True):
            st.code(data_url, language=None)
            st.success("✅ URL displayed above! Select and copy it.")
        
        # Info about data URLs
        st.info(
            "💡 **Note:** This is a data URL that embeds the image directly. "
            "You can paste it into a browser's address bar or use it in HTML/Markdown. "
            "For large images, consider using an image hosting service instead."
        )
        
        # Download button
        st.download_button(
            label="⬇️ Download Image",
            data=img_bytes,
            file_name=uploaded_file.name,
            mime=mime_type,
            use_container_width=True
        )

else:
    # Show placeholder when no image is uploaded
    st.info("👆 Upload an image to get started!")
    
    # Add example/instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload an image** using the file uploader above
        2. **Preview** your image on the left side
        3. **Copy the URL** from the right side to share with others
        4. **Paste the URL** in a browser address bar or embed it in HTML/Markdown
        
        **Supported formats:** PNG, JPG, JPEG, GIF, BMP, WEBP
        
        **Note:** The URL is a data URL that contains the entire image encoded in base64.
        For very large images, the URL might be very long.
        """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ By Dhruv Pandya")

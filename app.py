import streamlit as st
from fpdf import FPDF
from PIL import Image 
import os
import zipfile

st.set_page_config(page_title="Simple File Converter App", page_icon="📝")

st.title("Simple File Converter App")
st.subheader("Convert a .txt file to PDF")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("File content", text, height=200)

    if st.button("Convert to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_output = "converted_file.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="converted_file.pdf",
                mime="application/pdf"
            )


def compress_image(uploaded_file, quality=70):
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    base = os.path.splitext(uploaded_file.name)[0]
    out_path = os.path.join(temp_dir, f"compressed_{base}.jpg")
    img.save(out_path, format="JPEG", optimize=True, quality=int(quality))
    return out_path

st.markdown("---")
st.subheader("🖼️ Image Compressor (JPG/PNG)")

uploaded_image = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

quality = st.slider("Select Compression Quality (%)", 10, 95, 70)

if st.button("Compress Image"):
    if uploaded_image is not None:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        compressed_path = compress_image(uploaded_image, quality)
        with open(compressed_path, "rb") as file:
            st.download_button(
                label="Download Compressed Image",
                data=file,
                file_name=os.path.basename(compressed_path),
                mime="image/jpeg"
            )
        st.success("Image compressed successfully!")
    else:
        st.error("Please upload an image.")


st.markdown("---")
st.subheader("🖼️ Convert Image(s) to PDF")
image_files = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
if st.button("Convert to PDF"):
    if image_files:
        pdf = FPDF()
        for img_file in image_files:
            img = Image.open(img_file)
            img = img.convert("RGB")
            temp_path = f"temp_image.jpg"
            img.save(temp_path)
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=190)
        output_path = "images_to_pdf.pdf"
        pdf.output(output_path)
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="images_to_pdf.pdf",
                mime="application/pdf"
            )
        st.success("Images converted to PDF!")
    else:
        st.error("Please upload at least one image.")


st.markdown("---")
st.subheader("📦 ZIP Multiple Files")
zip_files = st.file_uploader("Upload multiple files to ZIP", accept_multiple_files=True)
if st.button("Create ZIP"):
    if zip_files:
        zip_filename = "compressed_files.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for file in zip_files:
                zipf.writestr(file.name, file.read())

        with open(zip_filename, "rb") as f:
            st.download_button(
                label="Download ZIP File",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )
        st.success("ZIP file created successfully!")
    else:
        st.error("Please upload files to zip.")

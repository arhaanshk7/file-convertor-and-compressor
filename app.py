import streamlit as st
from fpdf import FPDF
from PIL import Image
import os
import zipfile
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import time

# ------------------------ PAGE CONFIG ------------------------
st.set_page_config(
    page_title="File Converter & Compressor",
    page_icon="🧩",
    layout="wide"
)

# ------------------------ THEME TOGGLE ------------------------
theme = st.radio("Choose Theme:", ["Dark 🌑", "Light ☀️"], horizontal=True)

if theme == "Dark 🌑":
    bg_color = "linear-gradient(135deg, #1f1c2c, #928DAB)"
    text_color = "white"
    button_color = "#4CAF50"
    button_hover = "#45a049"
    download_button = "#008CBA"
    download_hover = "#007bb5"
    textarea_bg = "#2e2e2e"
    textarea_text = "white"
else:
    bg_color = "linear-gradient(135deg, #f5f7fa, #c3cfe2)"
    text_color = "black"
    button_color = "#4CAF50"
    button_hover = "#45a049"
    download_button = "#008CBA"
    download_hover = "#007bb5"
    textarea_bg = "#ffffff"
    textarea_text = "black"

# ------------------------ DYNAMIC CSS ------------------------
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_color};
        color: {text_color};
    }}
    h1, h2, h3, h4 {{
        color: {text_color} !important;
        text-align: center;
    }}
    .stButton>button {{
        background-color: {button_color};
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {button_hover};
        transform: scale(1.03);
    }}
    .stDownloadButton>button {{
        background-color: {download_button};
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }}
    .stDownloadButton>button:hover {{
        background-color: {download_hover};
        transform: scale(1.03);
    }}
    .stTextArea textarea {{
        background-color: {textarea_bg};
        color: {textarea_text};
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------ HEADER ------------------------
st.title("🧩 File Converter & Compressor")
st.markdown("<h4>Convert, Compress, Merge & Manage Files Easily</h4>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------ TXT TO PDF ------------------------
st.header("📄 Convert .TXT to PDF")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"], key="txt_upload")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("Preview File Content", text, height=200)
    
    if st.button("Convert to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_output = "converted_file.pdf"
        pdf.output(pdf_output)
        
        # Compression stats
        original_size = len(text.encode('utf-8')) / 1024
        compressed_size = os.path.getsize(pdf_output) / 1024
        st.metric("Original Size (KB)", f"{original_size:.2f}")
        st.metric("PDF Size (KB)", f"{compressed_size:.2f}")
        st.metric("Size Saved (%)", f"{100 - (compressed_size/original_size*100):.2f}%")
        
        with open(pdf_output, "rb") as file:
            st.download_button("⬇️ Download PDF", data=file, file_name="converted_file.pdf", mime="application/pdf")

st.markdown("---")

# ------------------------ IMAGE COMPRESSOR ------------------------
st.header("🖼️ Image Compressor (Batch Supported)")
uploaded_images = st.file_uploader("Upload image(s) (JPG/PNG)", type=["jpg","jpeg","png"], accept_multiple_files=True)
quality = st.slider("Select Compression Quality (%)", 10, 95, 70)

def compress_image(uploaded_file, quality=70):
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    os.makedirs("temp", exist_ok=True)
    base = os.path.splitext(uploaded_file.name)[0]
    out_path = os.path.join("temp", f"compressed_{base}.jpg")
    img.save(out_path, format="JPEG", optimize=True, quality=int(quality))
    return out_path

if st.button("Compress Image(s)"):
    if uploaded_images:
        st.info("Compressing images...")
        progress = st.progress(0)
        compressed_files = []
        for i, img_file in enumerate(uploaded_images):
            time.sleep(0.1)
            compressed_path = compress_image(img_file, quality)
            compressed_files.append(compressed_path)
            progress.progress(int((i+1)/len(uploaded_images)*100))
        st.success("✅ Compression Complete!")
        for path in compressed_files:
            orig_size = os.path.getsize(path.replace("compressed_", ""))/1024 if os.path.exists(path.replace("compressed_", "")) else 0
            new_size = os.path.getsize(path)/1024
            st.image(path, caption=f"{os.path.basename(path)} | Original: {orig_size:.2f}KB | Compressed: {new_size:.2f}KB")
            with open(path, "rb") as f:
                st.download_button("⬇️ Download", data=f, file_name=os.path.basename(path), mime="image/jpeg")
    else:
        st.error("Please upload at least one image.")

st.markdown("---")

# ------------------------ IMAGE(S) TO PDF ------------------------
st.header("🖼️ Convert Image(s) to PDF")
image_files = st.file_uploader("Upload image(s)", type=["jpg","jpeg","png"], accept_multiple_files=True, key="images_to_pdf")
if st.button("Convert Images to PDF"):
    if image_files:
        pdf = FPDF()
        st.info("Converting images to PDF...")
        progress = st.progress(0)
        for i, img_file in enumerate(image_files):
            img = Image.open(img_file).convert("RGB")
            temp_path = "temp_image.jpg"
            img.save(temp_path)
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=190)
            progress.progress(int((i+1)/len(image_files)*100))
        output_path = "images_to_pdf.pdf"
        pdf.output(output_path)
        with open(output_path, "rb") as file:
            st.download_button("⬇️ Download PDF", data=file, file_name="images_to_pdf.pdf", mime="application/pdf")
        st.success("✅ Images converted to PDF!")
    else:
        st.error("Please upload at least one image.")

st.markdown("---")

# ------------------------ ZIP MULTIPLE FILES ------------------------
st.header("📦 ZIP Multiple Files")
zip_files = st.file_uploader("Upload multiple files to ZIP", accept_multiple_files=True, key="zip_upload")
if st.button("Create ZIP File"):
    if zip_files:
        zip_filename = "compressed_files.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for file in zip_files:
                zipf.writestr(file.name, file.read())
        with open(zip_filename, "rb") as f:
            st.download_button("⬇️ Download ZIP File", data=f, file_name=zip_filename, mime="application/zip")
        st.success("✅ ZIP file created successfully!")
    else:
        st.error("Please upload files to zip.")

st.markdown("---")

# ------------------------ PDF MERGE/SPLIT ------------------------
st.header("📄 PDF Merge / Split")
pdf_files = st.file_uploader("Upload PDF(s) for Merge/Split", type=["pdf"], accept_multiple_files=True, key="pdf_merge")
merge_option = st.radio("Choose Operation", ["Merge PDFs", "Split PDF"], horizontal=True)

if st.button("Run PDF Operation"):
    if pdf_files:
        if merge_option == "Merge PDFs":
            merger = PdfMerger()
            for pdf_file in pdf_files:
                merger.append(pdf_file)
            merged_file = "merged.pdf"
            merger.write(merged_file)
            merger.close()
            with open(merged_file, "rb") as f:
                st.download_button("⬇️ Download Merged PDF", data=f, file_name="merged.pdf", mime="application/pdf")
            st.success("✅ PDFs merged successfully!")
        else:  # Split PDF
            pdf_reader = PdfReader(pdf_files[0])
            for i, page in enumerate(pdf_reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                split_file = f"page_{i+1}.pdf"
                with open(split_file, "wb") as f_out:
                    writer.write(f_out)
                with open(split_file, "rb") as f_in:
                    st.download_button(f"⬇️ Download Page {i+1}", data=f_in, file_name=split_file, mime="application/pdf")
            st.success("✅ PDF split successfully!")

# ------------------------ CLEANUP TEMP FILES ------------------------
# Optional: delete

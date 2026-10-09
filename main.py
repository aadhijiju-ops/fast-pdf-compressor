import io
import fitz  # PyMuPDF
import streamlit as st


def compress_pdf(input_bytes: bytes) -> bytes:
    """
    Compresses PDF data from memory by removing duplicate objects (garbage collection)
    and compressing text/image data streams.
    """
    # Load the PDF from memory bytes
    doc = fitz.open(stream=input_bytes, filetype="pdf")

    # Create a buffer to save the compressed version
    output_buffer = io.BytesIO()

    # Save with optimizations:
    # deflate=True compresses streams, garbage=4 removes duplicate/unused objects
    doc.save(
        output_buffer,
        garbage=4,
        deflate=True,
        clean=True
    )

    doc.close()
    return output_buffer.getvalue()


# --- Streamlit Frontend Configuration ---
st.set_page_config(page_title="Fast PDF Compressor", page_icon="📄")
st.title("⚡ Fast PDF Compressor")
st.write("Upload any PDF to compress its size instantly using PyMuPDF.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Read file into memory bytes
    file_bytes = uploaded_file.read()
    initial_size = len(file_bytes) / 1024  # KB

    st.info(f"Original Size: **{initial_size:.2f} KB**")

    with st.spinner("Compressing..."):
        # Perform in-memory compression
        compressed_bytes = compress_pdf(file_bytes)
        final_size = len(compressed_bytes) / 1024  # KB

    # Calculate savings
    savings = initial_size - final_size
    percent_saved = (savings / initial_size) * 100 if initial_size > 0 else 0

    st.success(f"Compressed Size: **{final_size:.2f} KB** (Saved **{percent_saved:.1f}%**)")

    # Provide a direct download button
    st.download_button(
        label="📥 Download Compressed PDF",
        data=compressed_bytes,
        file_name=f"compressed_{uploaded_file.name}",
        mime="application/pdf"
    )
import streamlit as st
from huffman import compress, decompress
import tempfile

st.title("Huffman Compressor/Decompressor")

mode = st.radio("Choose Mode", ["Compress", "Decompress"])

uploaded_file = st.file_uploader("Upload a file", type=["txt"])

if uploaded_file:
    input_text = uploaded_file.read().decode("utf-8")

    if mode == "Compress":
        compressed_data = compress(input_text)

        st.success("File compressed successfully!")
        st.download_button(
            label="Download Compressed File",
            data=compressed_data,
            file_name="compressed.huff",
            mime="text/plain"
        )

    else:  # Decompress
        try:
            decompressed_data = decompress(input_text)
            st.success("File decompressed successfully!")
            st.download_button(
                label="Download Decompressed File",
                data=decompressed_data,
                file_name="decompressed.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Decompression failed: {str(e)}")

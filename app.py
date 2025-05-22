import streamlit as st
from huffman import compress, decompress

st.set_page_config(page_title="Huffman Compressor", layout="centered")

st.title("📦 Huffman Text Compressor / Decompressor")

mode = st.radio("Choose Mode", ["Compress", "Decompress"], horizontal=True)

if mode == "Compress":
    input_file = st.file_uploader("Upload a text file to compress", type=["txt"])
    
    if input_file:
        input_text = input_file.read().decode("utf-8")
        if input_text.strip() == "":
            st.warning("The uploaded file is empty.")
        else:
            compressed_data = compress(input_text)

            st.success("File compressed successfully!")
            st.download_button(
                label="⬇️ Download Compressed File",
                data=compressed_data,
                file_name="compressed.huff",
                mime="text/plain"
            )

elif mode == "Decompress":
    compressed_file = st.file_uploader("Upload a .huff compressed file", type=["huff", "txt"])

    if compressed_file:
        try:
            compressed_text = compressed_file.read().decode("utf-8")
            if compressed_text.strip() == "":
                st.warning("The uploaded file is empty.")
            else:
                decompressed_data = decompress(compressed_text)

                st.success("File decompressed successfully!")
                st.download_button(
                    label="⬇️ Download Decompressed File",
                    data=decompressed_data,
                    file_name="decompressed.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"❌ Decompression failed: {str(e)}")

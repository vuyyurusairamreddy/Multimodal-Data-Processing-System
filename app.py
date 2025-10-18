import streamlit as st
import os
from config import *
from utils.database import *
from utils.embeddings import *
from utils.query_handler import query_perplexity
from processors.text_processor import process_text_file
from processors.image_processor import process_image
from processors.audio_processor import process_audio, process_video
from processors.youtube_processor import process_youtube_video
import warnings
warnings.filterwarnings('ignore')

init_database()

st.set_page_config(page_title="Multimodal RAG System", layout="wide")

st.title("Multimodal Data Processing System")
st.write("Upload files and ask natural language queries to get intelligent answers from your knowledge base.")

tab1, tab2, tab3 = st.tabs(["Upload Files", "Ask Questions", "View Knowledge Base"])

with tab1:
    st.header("Upload Files")
    
    upload_type = st.radio("Select Upload Type:", ["File Upload", "YouTube URL"])
    
    if upload_type == "File Upload":
        uploaded_files = st.file_uploader(
            "Upload documents, images, audio, or video files",
            type=['pdf', 'docx', 'pptx', 'txt', 'md', 'png', 'jpg', 'jpeg', 'mp3', 'mp4', 'wav', 'm4a', 'avi', 'mov', 'mkv'],
            accept_multiple_files=True
        )
        
        if st.button("Process Uploaded Files"):
            if uploaded_files:
                progress_bar = st.progress(0)
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    
                    st.write(f"Processing: {uploaded_file.name}")
                    
                    try:
                        if file_extension in SUPPORTED_TEXT_FORMATS:
                            content = process_text_file(file_path, file_extension)
                            metadata = {'type': 'text'}
                        
                        elif file_extension in SUPPORTED_IMAGE_FORMATS:
                            content, metadata = process_image(file_path)
                            metadata['type'] = 'image'
                        
                        elif file_extension in SUPPORTED_AUDIO_FORMATS:
                            content, metadata = process_audio(file_path)
                            metadata['type'] = 'audio'
                        
                        elif file_extension in SUPPORTED_VIDEO_FORMATS:
                            content, metadata = process_video(file_path)
                            metadata['type'] = 'video'
                        
                        else:
                            st.error(f"Unsupported file type: {file_extension}")
                            continue
                        
                        embedding = generate_embedding(content)
                        
                        doc_id = insert_document(
                            uploaded_file.name,
                            file_extension,
                            content,
                            metadata,
                            embedding
                        )
                        
                        st.success(f"Successfully processed: {uploaded_file.name}")
                    
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                st.success("All files processed successfully")
            else:
                st.warning("Please upload at least one file")
    
    else:
        youtube_url = st.text_input("Enter YouTube URL:")
        
        if st.button("Process YouTube Video"):
            if youtube_url:
                with st.spinner("Downloading and processing YouTube video..."):
                    try:
                        content, metadata = process_youtube_video(youtube_url, UPLOAD_DIR)
                        
                        embedding = generate_embedding(content)
                        
                        filename = metadata.get('title', 'youtube_video')
                        
                        doc_id = insert_document(
                            filename,
                            '.youtube',
                            content,
                            metadata,
                            embedding
                        )
                        
                        st.success(f"Successfully processed YouTube video: {filename}")
                    
                    except Exception as e:
                        st.error(f"Error processing YouTube video: {str(e)}")
            else:
                st.warning("Please enter a YouTube URL")

with tab2:
    st.header("Ask Questions")
    
    user_query = st.text_area("Enter your question:", height=100)
    
    if st.button("Get Answer"):
        if user_query:
            with st.spinner("Searching knowledge base and generating answer..."):
                documents = get_all_documents()
                
                if not documents:
                    st.warning("No documents in knowledge base. Please upload files first.")
                else:
                    relevant_docs = find_relevant_documents(user_query, documents, top_k=3)
                    
                    answer = query_perplexity(user_query, relevant_docs)
                    
                    st.subheader("Answer:")
                    st.write(answer)
                    
                    if relevant_docs:
                        st.subheader("Relevant Documents:")
                        for doc in relevant_docs:
                            with st.expander(f"Document: {doc['filename']}"):
                                st.write(doc['content'][:500] + "...")
                    
                    save_query(user_query, answer, [doc['filename'] for doc in relevant_docs])
        else:
            st.warning("Please enter a question")
    
    st.divider()
    
    st.subheader("Recent Queries")
    history = get_query_history(5)
    
    for query, response, timestamp in history:
        with st.expander(f"Query: {query[:50]}... ({timestamp})"):
            st.write(f"**Question:** {query}")
            st.write(f"**Answer:** {response}")

with tab3:
    st.header("Knowledge Base")
    
    documents = get_all_documents()
    
    st.write(f"Total documents: {len(documents)}")
    
    if documents:
        for doc in documents:
            with st.expander(f"{doc['filename']} ({doc['file_type']})"):
                st.write(f"**Type:** {doc['metadata'].get('type', 'unknown')}")
                st.write(f"**Content Preview:**")
                st.write(doc['content'][:500] + "...")
    else:
        st.info("No documents in knowledge base yet. Upload files to get started.")

st.sidebar.header("System Information")
st.sidebar.write(f"LLM: Perplexity API - {PERPLEXITY_MODEL}")
st.sidebar.write(f"Embedding Model: all-MiniLM-L6-v2")
st.sidebar.write(f"Database: SQLite")

docs_count = len(get_all_documents())
st.sidebar.metric("Documents Processed", docs_count)

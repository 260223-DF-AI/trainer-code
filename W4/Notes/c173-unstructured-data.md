# Unstructured Data

## Learning Objectives

- Define unstructured data and its characteristics
- Identify types of unstructured data and their sources
- Understand challenges in storing and processing unstructured content
- Learn strategies for extracting value from unstructured data

## Why This Matters

Unstructured data makes up approximately 80% of enterprise data. Emails, documents, images, videos, and social media posts contain valuable insights that organizations are just beginning to harness. Understanding unstructured data opens doors to advanced analytics, AI/ML applications, and competitive advantages.

## Concept Explanation

### What is Unstructured Data?

Unstructured data is information that does not follow a predefined data model or schema. It cannot be easily organized into rows and columns and requires specialized processing to extract meaning.

**Key Characteristics:**

- No predefined schema or structure
- Difficult to search with traditional SQL
- Often stored as files or blobs
- Requires parsing/interpretation to analyze
- Human-created or machine-generated

### Types of Unstructured Data

```
+------------------+     +------------------+     +------------------+
|      Text        |     |      Media       |     |      Other       |
+------------------+     +------------------+     +------------------+
| Emails           |     | Images           |     | Sensor data      |
| Documents        |     | Audio            |     | Satellite data   |
| Social media     |     | Video            |     | Scientific data  |
| Chat logs        |     | Medical scans    |     | Radar/lidar      |
| Web pages        |     | Security footage |     | Geospatial       |
+------------------+     +------------------+     +------------------+
```

### Sources and Volume

| Source | Examples | Daily Volume |
|--------|----------|--------------|
| Email | Corporate communications | 300 billion emails |
| Social Media | Tweets, posts, comments | 500 million tweets |
| Documents | PDFs, Word, presentations | Billions of files |
| Images | Photos, graphics, scans | 3.2 billion shared |
| Video | Streaming, surveillance | 1 million hours uploaded |
| Audio | Calls, podcasts, meetings | Millions of hours |

### Storage Challenges

**Volume:**

- A single HD video can be 10+ GB
- Organizations store petabytes of unstructured content
- Growth rate exceeds structured data

**Access Patterns:**

- Write once, read occasionally
- Full file access (not partial)
- No point queries like SQL

**Common Storage Solutions:**

| Storage Type | Examples | Use Case |
|--------------|----------|----------|
| Object Storage | S3, GCS, Azure Blob | General unstructured |
| File Systems | NFS, HDFS | Document repositories |
| Content Management | SharePoint, Box | Enterprise documents |
| Media Servers | Vimeo, YouTube | Video streaming |

### Processing Challenges

**Extracting Meaning:**
Unlike structured data with clear columns, unstructured data requires interpretation:

```
Structured:     price = 29.99  (immediate access)

Unstructured:   "The widget costs about thirty bucks"
                  - Parse text
                  - Identify price mention
                  - Extract numeric value
                  - Handle approximation
```

**Techniques for Processing:**

| Data Type | Technique | Output |
|-----------|-----------|--------|
| Text | NLP, NER | Entities, sentiment, topics |
| Images | Computer Vision | Objects, faces, text (OCR) |
| Audio | Speech-to-Text | Transcripts |
| Video | Frame analysis | Objects, actions, subtitles |
| Documents | Document AI | Structured fields |

### Making Unstructured Data Useful

#### 1. Metadata Enrichment

Add structured metadata about unstructured content:

```json
{
  "file_path": "/documents/contracts/acme-2024.pdf",
  "file_type": "application/pdf",
  "size_bytes": 245760,
  "created_at": "2024-01-15T10:30:00Z",
  "author": "legal@company.com",
  "extracted_entities": {
    "company_names": ["Acme Corp", "WidgetCo"],
    "dates": ["2024-01-01", "2025-12-31"],
    "amounts": [50000, 75000]
  },
  "classification": "contract",
  "sentiment": "neutral",
  "keywords": ["agreement", "services", "payment terms"]
}
```

#### 2. Indexing for Search

Create searchable indexes from content:

- Full-text search engines (Elasticsearch)
- Vector embeddings for semantic search
- Keyword extraction and tagging

#### 3. AI/ML Processing

Apply machine learning to extract structured insights:

- Named Entity Recognition (NER)
- Image classification and object detection
- Speech recognition and translation
- Document classification

## Code Example

Working with unstructured data in Python:

```python
import os
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UnstructuredDocument:
    """Represent an unstructured document with metadata."""
    file_path: str
    file_type: str
    size_bytes: int
    created_at: datetime
    content_text: str = ""
    extracted_entities: Dict = None
    embedding: List[float] = None

class UnstructuredDataProcessor:
    """Process and enrich unstructured data."""
    
    def __init__(self):
        self.supported_types = {
            '.txt': self._process_text,
            '.pdf': self._process_pdf,
            '.jpg': self._process_image,
            '.png': self._process_image,
        }
    
    def process_file(self, file_path: str) -> UnstructuredDocument:
        """Process an unstructured file."""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        # Basic metadata
        stat = path.stat()
        doc = UnstructuredDocument(
            file_path=str(path),
            file_type=suffix,
            size_bytes=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime)
        )
        
        # Process based on type
        if suffix in self.supported_types:
            processor = self.supported_types[suffix]
            doc = processor(doc, path)
        
        return doc
    
    def _process_text(self, doc: UnstructuredDocument, path: Path) -> UnstructuredDocument:
        """Extract content from text file."""
        doc.content_text = path.read_text(encoding='utf-8', errors='ignore')
        doc.extracted_entities = self._extract_entities_from_text(doc.content_text)
        return doc
    
    def _process_pdf(self, doc: UnstructuredDocument, path: Path) -> UnstructuredDocument:
        """Extract content from PDF."""
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text())
            doc.content_text = "\n".join(text_parts)
            doc.extracted_entities = self._extract_entities_from_text(doc.content_text)
        except ImportError:
            doc.content_text = "[PDF processing requires pypdf library]"
        return doc
    
    def _process_image(self, doc: UnstructuredDocument, path: Path) -> UnstructuredDocument:
        """Extract metadata and text from image."""
        try:
            from PIL import Image
            import pytesseract
            
            # Get image metadata
            img = Image.open(path)
            doc.extracted_entities = {
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format
            }
            
            # OCR for text extraction
            doc.content_text = pytesseract.image_to_string(img)
        except ImportError:
            doc.extracted_entities = {"note": "PIL/tesseract required for full processing"}
        return doc
    
    def _extract_entities_from_text(self, text: str) -> Dict:
        """Extract basic entities from text."""
        import re
        
        entities = {
            "emails": re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text),
            "urls": re.findall(r'https?://\S+', text),
            "phone_numbers": re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text),
            "dates": re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', text),
            "dollar_amounts": re.findall(r'\$[\d,]+(?:\.\d{2})?', text),
            "word_count": len(text.split())
        }
        
        return entities
    
    def create_search_index(self, documents: List[UnstructuredDocument]) -> Dict:
        """Create simple inverted index for text search."""
        index = {}
        
        for doc in documents:
            words = doc.content_text.lower().split()
            for word in set(words):  # Unique words only
                if len(word) > 2:  # Skip short words
                    if word not in index:
                        index[word] = []
                    index[word].append(doc.file_path)
        
        return index


# Example: Processing a directory of unstructured files
def process_document_directory(directory: str):
    """Process all documents in a directory."""
    processor = UnstructuredDataProcessor()
    documents = []
    
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            try:
                doc = processor.process_file(str(file_path))
                documents.append(doc)
                print(f"Processed: {doc.file_path}")
                print(f"  Type: {doc.file_type}")
                print(f"  Size: {doc.size_bytes:,} bytes")
                if doc.extracted_entities:
                    print(f"  Entities: {doc.extracted_entities}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    # Build search index
    search_index = processor.create_search_index(documents)
    print(f"\nBuilt search index with {len(search_index)} unique terms")
    
    return documents, search_index
```

## Key Takeaways

- Unstructured data (~80% of enterprise data) lacks predefined schema
- Common types include text documents, emails, images, audio, and video
- Object storage (S3, GCS) is the standard for unstructured data
- Processing requires AI/ML techniques: NLP, computer vision, speech recognition
- Metadata enrichment makes unstructured data searchable and analyzable
- The value in unstructured data is unlocked through extraction and indexing

## Resources

- Google Cloud Document AI: <https://cloud.google.com/document-ai>
- Amazon Textract: <https://aws.amazon.com/textract/>
- Elasticsearch: <https://www.elastic.co/elasticsearch/>
- OpenAI Embeddings: <https://platform.openai.com/docs/guides/embeddings>

from googleapiclient.discovery import build
from django.conf import settings
from typing import Dict, List, Optional
import logging
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class GoogleBooksService:
    def __init__(self):
        api_key = settings.GOOGLE_BOOKS_API_KEY
        logger.info(f"Google Books API key configured: {'Yes' if api_key else 'No'}")
        if not api_key:
            logger.error("Google Books API key is not configured. Please set GOOGLE_BOOKS_API_KEY in your environment variables.")
            raise ValueError("Google Books API key is not configured")
        try:
            logger.info("Initializing Google Books service...")
            self.service = build('books', 'v1', developerKey=api_key)
            logger.info("Google Books service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Books service: {str(e)}")
            raise
    
    def search_books(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for books using the Google Books API
        Args:
            query: Search query string (can include subject: prefix for category searches)
            max_results: Maximum number of results to return
        """
        try:
            logger.info(f"Searching Google Books for query: {query}")
            
            # If the query already includes subject: prefix, use it as is
            if 'subject:' in query:
                search_query = query
            else:
                search_query = query
            
            result = self.service.volumes().list(
                q=search_query,
                maxResults=max_results,
                printType='BOOKS',
                orderBy='relevance'  # Sort by relevance
            ).execute()
            
            books = []
            for item in result.get('items', []):
                volume_info = item.get('volumeInfo', {})
                book = {
                    'title': volume_info.get('title', ''),
                    'authors': volume_info.get('authors', []),
                    'publisher': volume_info.get('publisher', ''),
                    'published_date': volume_info.get('publishedDate', ''),
                    'description': volume_info.get('description', ''),
                    'isbn': self._extract_isbn(volume_info.get('industryIdentifiers', [])),
                    'page_count': volume_info.get('pageCount'),
                    'categories': volume_info.get('categories', []),
                    'image_url': self._get_image_url(volume_info.get('imageLinks', {})),
                    'google_books_id': item.get('id')
                }
                books.append(book)
            logger.info(f"Found {len(books)} books")
            return books
        except HttpError as e:
            logger.error(f"Google Books API error: {str(e)}")
            if e.resp.status == 403:
                raise ValueError("Invalid or missing API key")
            elif e.resp.status == 429:
                raise ValueError("API quota exceeded")
            else:
                raise
        except Exception as e:
            logger.error(f"Error searching Google Books: {str(e)}")
            raise
    
    def get_book_details(self, google_books_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific book
        """
        try:
            result = self.service.volumes().get(volumeId=google_books_id).execute()
            volume_info = result.get('volumeInfo', {})
            return {
                'title': volume_info.get('title', ''),
                'authors': volume_info.get('authors', []),
                'publisher': volume_info.get('publisher', ''),
                'published_date': volume_info.get('publishedDate', ''),
                'description': volume_info.get('description', ''),
                'isbn': self._extract_isbn(volume_info.get('industryIdentifiers', [])),
                'page_count': volume_info.get('pageCount'),
                'categories': volume_info.get('categories', []),
                'image_url': self._get_image_url(volume_info.get('imageLinks', {})),
                'google_books_id': google_books_id
            }
        except Exception as e:
            print(f"Error getting book details: {str(e)}")
            return None
    
    def _extract_isbn(self, identifiers: List[Dict]) -> str:
        """
        Extract ISBN from industry identifiers
        """
        for identifier in identifiers:
            if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                return identifier.get('identifier', '')
        return ''
    
    def _get_image_url(self, image_links: Dict) -> str:
        """
        Get the best available image URL
        """
        if image_links.get('thumbnail'):
            return image_links['thumbnail'].replace('http://', 'https://')
        elif image_links.get('smallThumbnail'):
            return image_links['smallThumbnail'].replace('http://', 'https://')
        return ''
    
    def get_categories(self) -> List[str]:
        """
        Get a list of common book categories from Google Books
        """
        try:
            # Common categories in Google Books
            common_categories = [
                "Fiction", "Nonfiction", "Science", "History", "Biography",
                "Technology", "Art", "Business", "Computers", "Cooking",
                "Education", "Health & Fitness", "Humor", "Law", "Mathematics",
                "Medical", "Philosophy", "Psychology", "Religion", "Science Fiction",
                "Self-Help", "Sports", "Travel"
            ]
            return sorted(common_categories)
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return [] 

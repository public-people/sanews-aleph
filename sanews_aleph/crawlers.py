from aleph.crawlers import DocumentCrawler
from sanews.models import Article
from sanews import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from slugify import slugify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TheNewAgeCrawler(DocumentCrawler):
    SCHEDULE = DocumentCrawler.DAILY
    COLLECTION_ID = 'thenewage'
    COLLECTION_LABEL = 'The New Age'

    def __init__(self, *args, **kwargs):
        super(TheNewAgeCrawler, self).__init__(*args, **kwargs)

        engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=engine)

    def crawl(self):
        session = self.Session()
        try:
            publication_filter = Article.publication_name == self.COLLECTION_LABEL
            for article in session.query(Article).filter(publication_filter):
                self.crawl_document(article)
        except:
            raise
        finally:
            session.close()

    def crawl_document(self, article):
        local_path = '/data/ingest/sanews/%s' % slugify(article['url'])
        with open(local_path) as file:
            file.write(article['body_html'])
        document = self.create_document(foreign_id=article['url'])
        document.source_url = article.get('url')
        document.title = article.get('title')
        document.add_date(article.get('publication_date').isoformat())
        document.mime_type = 'text/html'
        self.emit_file(document, local_path)

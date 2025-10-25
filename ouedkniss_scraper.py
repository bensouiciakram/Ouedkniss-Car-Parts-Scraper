"""
Ouedkniss Car Parts Scraper

This Scrapy-based project scrapes car parts listings from Ouedkniss.com, extracting detailed information about each announcement, including seller, phone, comments, and more. The spider uses GraphQL endpoints and paginates through all available listings in the 'pieces_detachees' category.

Author: Project Developer
License: MIT
"""

import scrapy 
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess 
from scrapy import Request 
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader
import json 
from copy import deepcopy 
from typing import List, Dict, Any, Optional

class DetailsItem(scrapy.Item):
    """
    Scrapy Item for storing details of a single Ouedkniss announcement.
    """
    page_number = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    likes_number = scrapy.Field(
        output_processor=TakeFirst()
    )
    announcement_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    published_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    vues_number = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
    phone = scrapy.Field(
        #output_processor=TakeFirst()
    )
    regions = scrapy.Field(
        #output_processor=TakeFirst()
    )
    seller_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    boutique_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    first_10_comments = scrapy.Field(
        #output_processor=TakeFirst()
    )

class InfosSpider(scrapy.Spider):
    """
    Spider for scraping car parts announcements from Ouedkniss.com using GraphQL endpoints.
    """
    name = 'extractor'  
    annoucement_url_template = 'https://www.ouedkniss.com/{slug}-d{annoucement_id}'
    headers = {
        'content-type': 'application/json',
    }
    # json_data = {
    #     'operationName': 'SearchQuery',
    #     'variables': {
    #         'mediaSize': 'MEDIUM',
    #         'q': None,
    #         'filter': {
    #             'categorySlug': 'pieces_detachees',
    #             'origin': None,
    #             'connected': False,
    #             'delivery': None,
    #             'regionIds': [],
    #             'cityIds': [],
    #             'priceRange': [
    #                 None,
    #                 None,
    #             ],
    #             'exchange': False,
    #             'hasPictures': False,
    #             'hasPrice': False,
    #             'priceUnit': None,
    #             'fields': [],
    #             'page': 1,
    #             'count': 48,
    #         },
    #     },
    #     'query': 'query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  priceType\n  exchangeType\n  __typename\n}\n',
    # }

    json_data = json_data = {
    'operationName': 'SearchQuery',
    'variables': {
        'mediaSize': 'MEDIUM',
        'q': None,
        'filter': {
            'categorySlug': 'pieces_detachees',
            'origin': None,
            'connected': False,
            'delivery': None,
            'regionIds': [],
            'cityIds': [],
            'priceRange': [],
            'exchange': None,
            'hasPictures': False,
            'hasPrice': False,
            'priceUnit': None,
            'fields': [],
            'page': 1,
            'orderByField': {
                'field': 'REFRESHED_AT',
            },
            'count': 48,
        },
    },
    'query': 'query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        isWithoutExchange\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          slug\n          __typename\n        }\n        __typename\n      }\n      count\n      filter {\n        cities {\n          id\n          name\n          __typename\n        }\n        regions {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  paymentMethod\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    viewAsStore\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}',
}

    user_json_data = {
        'operationName': 'AnnouncementGet',
        'variables': {
            'id': '51585809',
        },
        'query': 'query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    oldPricePreview\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      id\n      slug\n      name\n      deliveryType\n      parentTree {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      parentId\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      viewAsStore\n      announcementsCount\n      status\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      pricePreview\n      oldPricePreview\n      quantity\n      __typename\n    }\n    showAnalytics\n    messengerLink\n    __typename\n  }\n}',
    }


    phone_json_data = {
        'operationName': 'UnhidePhone',
        'variables': {
            'id': '51585809',
        },
        'query': 'query UnhidePhone($id: ID!) {\n  phones: announcementPhoneGet(id: $id) {\n    id\n    phone\n    phoneExt\n    hasViber\n    hasWhatsapp\n    hasTelegram\n    __typename\n  }\n}',
    }

    comment_json_data = {
        'operationName': 'AnnouncementCommentsGet',
        'variables': {
            'first': 10,
            'id': '36319784',
            'page': 1,
        },
        'query': 'query AnnouncementCommentsGet($id: ID!, $first: Int = 10, $page: Int!) {\n  commentsList: announcementCommentList(\n    announcementId: $id\n    first: $first\n    page: $page\n    orderBy: {column: CREATED_AT, order: DESC}\n  ) {\n    data {\n      id\n      createdAt\n      content\n      likesCount\n      dislikesCount\n      iReported\n      user {\n        id\n        username\n        displayName\n        avatarUrl\n        __typename\n      }\n      store {\n        id\n        name\n        slug\n        imageUrl\n        __typename\n      }\n      replies {\n        id\n        createdAt\n        content\n        likesCount\n        dislikesCount\n        iReported\n        user {\n          id\n          username\n          displayName\n          avatarUrl\n          __typename\n        }\n        store {\n          id\n          name\n          slug\n          imageUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    paginatorInfo {\n      hasMorePages\n      __typename\n    }\n    __typename\n  }\n}',
    }

    reactions_json_data = {
        'operationName': 'AnnouncementReactions',
        'variables': {
            'id': '51585809',
        },
        'query': 'query AnnouncementReactions($id: ID!) {\n  reactions: announcementDetails(id: $id) {\n    id\n    viewCount\n    likeCount\n    userReaction {\n      isBookmarked\n      isLiked\n      __typename\n    }\n    __typename\n  }\n}',
    }

    def __init__(self,listing_url:str,initial_page:int,last_page:int):
        """
        Initialize the spider with the listing URL and page range.
        Args:
            listing_url (str): The base URL for the listing.
            initial_page (int): The first page to scrape.
            last_page (int): The last page to scrape.
        """
        self.listing_url = listing_url
        self.initial_page = initial_page 
        self.last_page = last_page 

    def start_requests(self):
        """
        Start the scraping process by requesting the first page to determine the total number of pages.
        """
        yield Request(
            'https://api.ouedkniss.com/graphql',
            headers=self.headers,
            body = json.dumps(
                self.configure_listing_payload(
                    1,
                    self.get_cateogory_slug()
                )
            ),
            method='POST',
            callback=self.parse_pages_range       
        )

    def parse_pages_range(self,response):
        """
        Parse the response to determine the total number of pages and queue requests for each page.
        """
        total_pages = self.get_total_pages(response)
        for page in range(self.initial_page,self.last_page + 1) :
            yield Request(
                'https://api.ouedkniss.com/graphql',
                headers=self.headers, 
                body = json.dumps(
                    self.configure_listing_payload(
                        page,
                        self.get_cateogory_slug()
                    )
                ),
                dont_filter=True,
                method='POST',
                callback=self.parse_annoucements,
                meta = {
                    'page':page
                }
            )


#parse_annoucements
    def parse_annoucements(self,response):
        """
        Parse the announcements on a page and queue requests for details, phones, and user info.
        """
        announcements = response.json()['data']['search']['announcements']['data']
        for annoucement in announcements : 
            loader = ItemLoader(DetailsItem(),response)
            loader.add_value('page_number',response.meta['page'])
            loader.add_value('title',annoucement['title'])
            loader.add_value('likes_number',annoucement['likeCount'])
            loader.add_value('announcement_id',annoucement['id'])
            loader.add_value('published_date',annoucement['createdAt'])
            loader.add_value('vues_number','')
            loader.add_value('description',annoucement['description'])
            loader.add_value('regions',self.get_regions(annoucement))
            loader.add_value('boutique_name',self.get_store_name(annoucement))
            yield Request(
                'https://api.ouedkniss.com/graphql',
                headers=self.headers,
                body=json.dumps(
                    self.configure_phone_payload(annoucement['id'])
                ),
                callback=self.parse_phones,
                method='POST',
                dont_filter=True,
                meta={
                    'loader':loader,
                    'annoucement':annoucement
                }
            )

    def parse_phones(self,response):
        """
        Parse the phone numbers for an announcement and queue request for user name.
        """
        annoucement = response.meta['annoucement']
        loader = response.meta['loader']
        try :
            loader.add_value('phone',self.get_phones(response))
        except AttributeError :
            loader.add_value('phone',[])
        yield Request(
            'https://api.ouedkniss.com/graphql',
            headers=self.headers,
            body=json.dumps(
                self.configure_user_payload(annoucement['id'])
            ),
            callback=self.parse_user_name,
            dont_filter=True,
            method='POST',
            meta={
                'loader':loader,
                'annoucement':annoucement
            }
        )

    def parse_user_name(self,response):
        """
        Parse the seller name for an announcement and queue request for comments.
        """
        annoucement = response.meta['annoucement']
        loader = response.meta['loader']
        loader.add_value('seller_name',self.get_seller_name(response))
        self.headers['accept'] = '*/*'
        yield Request(
            'https://api.ouedkniss.com/graphql',
            headers=self.headers,
            body=json.dumps(
                self.configure_comment_payload(annoucement['id'])
            ),
            callback=self.parse_comments,
            dont_filter=True,
            method='POST',
            meta={
                'loader':loader,
                'annoucement':annoucement
            }
        )

    def parse_comments(self,response):
        """
        Parse the first 10 comments for an announcement and queue request for reactions.
        """
        annoucement = response.meta['annoucement']
        loader = response.meta['loader']
        if response.json()['data']['commentsList']['data'] :
            loader.add_value('first_10_comments',self.format_comments(response))
        yield Request(
            'https://api.ouedkniss.com/graphql',
            headers=self.headers,
            body=json.dumps(
                self.configure_reaction_payload(annoucement['id'])
            ),
            callback=self.parse_reactions,
            dont_filter=True,
            method='POST',
            meta={
                'loader':loader
            }
        )

    def parse_reactions(self,response):
        """
        Parse the reactions for an announcement and yield the final item.
        """
        loader = response.meta['loader']
        loader.add_value('vues_number',self.get_views_count(response))
        yield loader.load_item()

    def get_cateogory_slug(self) -> str:
        """
        Return the category slug for car parts listings.
        Returns:
            str: The category slug.
        """
        return 'pieces_detachees'


    def configure_listing_payload(self, page: int, cetegory_slug: str) -> dict:
        """
        Configure the payload for the listing GraphQL request.
        Args:
            page (int): The page number.
            cetegory_slug (str): The category slug.
        Returns:
            dict: The payload dictionary.
        """
        payload = deepcopy(self.json_data)
        payload['variables']['filter']['page'] = page
        payload['variables']['filter']['categorySlug'] = cetegory_slug
        return payload


    def configure_user_payload(self, annoucement_id: int) -> dict:
        """
        Configure the payload for the user GraphQL request.
        Args:
            annoucement_id (int): The announcement ID.
        Returns:
            dict: The payload dictionary.
        """
        payload = deepcopy(self.user_json_data)
        payload['variables']['id'] = str(annoucement_id)
        return payload


    def configure_phone_payload(self, annoucement_id: int) -> dict:
        """
        Configure the payload for the phone GraphQL request.
        Args:
            annoucement_id (int): The announcement ID.
        Returns:
            dict: The payload dictionary.
        """
        payload = deepcopy(self.phone_json_data)
        payload['variables']['id'] = str(annoucement_id)
        return payload

    def configure_comment_payload(self, annoucement_id: int) -> dict:
        """
        Configure the payload for the comments GraphQL request.
        Args:
            annoucement_id (int): The announcement ID.
        Returns:
            dict: The payload dictionary.
        """
        payload = deepcopy(self.comment_json_data)
        payload['variables']['id'] = str(annoucement_id)
        return payload

    def configure_reaction_payload(self, announcement_id:int) -> dict:
        """
        Configure the payload for the reactions GraphQL request.
        Args:
            announcement_id (int): The announcement ID.
        Returns:
            dict: The payload dictionary.
        """
        payload = deepcopy(self.reactions_json_data)
        payload['variables']['id'] = str(announcement_id)
        return payload

    def get_regions(self, annoucement: dict) -> list:
        """
        Extract the list of regions from an announcement.
        Args:
            annoucement (dict): The announcement dictionary.
        Returns:
            list: List of region names.
        """
        regions = []
        if 'cities' in annoucement and annoucement['cities']:
            for city in annoucement['cities']:
                if 'region' in city and city['region']:
                    regions.append(city['region']['name'])
        return regions

    def get_store_name(self, annoucement: dict) -> str:
        """
        Extract the store name from an announcement if available.
        Args:
            annoucement (dict): The announcement dictionary.
        Returns:
            str: The store name or an empty string.
        """
        if 'store' in annoucement and annoucement['store']:
            return annoucement['store'].get('name', '')
        return '' 
    
    def get_phones(self, response) -> List[str]:
        """
        Extract the list of phone numbers from the response.
        Args:
            response: A requests Response object containing JSON data.
        Returns:
            A list of phone numbers, as a list of strings.
        """
        phones = []
        data = response.json().get('data', {})
        phones_data = data.get('phones', [])
        for phone in phones_data:
            if 'phone' in phone:
                phones.append(phone['phone'])
        return phones


    def get_seller_name(self, response) -> str:
        """
        Extract the name of the seller from the response JSON.
        Args:
            response: A requests Response object containing JSON data.
        Returns:
            The name of the seller, as a string.
        """
        data = response.json().get('data', {})
        announcement = data.get('announcement', {})
        user = announcement.get('user', {})
        return user.get('displayName', '')
    
    def format_comments(self, response) -> str :
        """
        Format comments from the response object and return them as a formated string.
        Args:
            response (requests.Response): Response object containing the comments.
        Returns:
            formatted list of comments as one per line comment string.
        """
        comments = []
        data = response.json().get('data', {})
        comments_list = data.get('commentsList', {})
        for comment in comments_list.get('data', []):
            content = comment.get('content', '')
            user = comment.get('user', {})
            username = user.get('displayName', '')
            comments.append(f'{username}: {content}')
        return '\n'.join(comments)

    def get_total_pages(self, response) -> int:
        """
        Get the total number of pages from the listing page and return it as an integer.
        Args:
            response (requests.Response): Response object containing the total number of pages.
        Returns:
            int: Total number of pages.
        """
        paginator_info = response.json()['data']['search']['announcements']['paginatorInfo']
        return paginator_info.get('lastPage', 1)

    def parse_annoucement_url(self, annoucement: dict) -> str:
        """
        Parse the announcement URL using the provided announcement dictionary and return the URL as a string.
        Args:
            annoucement (dict): Dictionary containing the announcement data.
        Returns:
            str: The announcement URL.
        """
        return self.annoucement_url_template.format(
            slug=annoucement['slug'],
            annoucement_id=annoucement['id']
        )
    
    def get_views_count(self, response) -> int:
        """
        Extracts the view count from the given response object and returns it as an integer.
        Args:
            response (scrapy.Response): The response object containing the view count data.
        Returns:
            int: The view count as an integer.
        """
        data = response.json().get('data', {})
        reactions = data.get('reactions', {})
        return reactions.get('viewCount', 0)

if __name__ == '__main__':
    listing_url = "https://www.ouedkniss.com/pieces_detachees/1" #input('Past the your url : ')
    initial_page = 1 #int(input('Enter the first page id : '))    
    last_page = 2 #int(input('Enter the last page id : '))    
    process = CrawlerProcess(
        {
            'HTTPCACHE_ENABLED' : True,
            'FEED_URI':'output.csv',
            'FEED_FORMAT':'csv',
            #'COOKIES_ENABLED ':False,
            'HTTPERROR_ALLOWED_CODES':[404]
        }
    )

    process.crawl(InfosSpider,listing_url,initial_page,last_page)
    process.start()

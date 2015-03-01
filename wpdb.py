from sqlalchemy import Column, MetaData, Table
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, dynamic_loader, mapper, relation
from sqlalchemy.orm.collections import column_mapped_collection

class Term:
  def __init__(self, name, slug, term_group=0):
    self.name = name
    self.slug = slug
    self.term_group = term_group

  def __repr__(self):
    return '<Term(%r, %r, %r)>' % (self.name, self.slug, self.term_group)

class Taxonomy(object):
  def __init__(self, term, description):
    self.term = term
    self.description = description

class PostTag(Taxonomy):
  def __repr__(self):
    return '<PostTag(%r, %r)>' % (self.term, self.description)

class Category(Taxonomy):
  def __repr__(self):
    return '<Category(%r, %r)>' % (self.term, self.description)

class LinkCategory(Taxonomy):
  def __repr__(self):
    return '<LinkCategory(%r, %r)>' % (self.term, self.description)

class PostMeta(object):
  def __init__(self, meta_key, meta_value):
    self.meta_key = meta_key
    self.meta_value = meta_value

  def __repr__(self):
    return '<PostMeta(%r, %r)>' % (self.meta_key, self.meta_value)

class Post(object):
  def __init__(self, post_title, post_type='post'):
    self.post_title = post_title
    self.post_type = post_type
  
  meta = association_proxy('_metadict', 'meta_value', creator=PostMeta)

  def __repr__(self):
    return '<Post(%r, %r)>' % (self.post_title, self.post_type)

class Link(object):
  def __init__(self, link_url, link_name):
    self.link_url = link_url
    self.link_name = link_name

  def __repr__(self):
    return '<Link(%r, %r)>' % (self.link_url, self.link_name)

class CommentMeta(object):
  def __init__(self, meta_key, meta_value):
    self.meta_key = meta_key
    self.meta_value = meta_value

  def __repr__(self):
    return '<CommentMeta(%r, %r)>' % (self.meta_key, self.meta_value)

class Comment(object):
  def __init__(self, comment_author, comment_content):
    self.comment_author = comment_author
    self.comment_content = comment_content
  
  meta = association_proxy('_metadict', 'meta_value', creator=CommentMeta)

  def __repr__(self):
    return '<Comment(%r, %r)>' % (self.comment_author, self.comment_content)

class UserMeta(object):
  def __init__(self, meta_key, meta_value):
    self.meta_key = meta_key
    self.meta_value = meta_value

  def __repr__(self):
    return '<UserMeta(%r, %r)>' % (self.meta_key, self.meta_value)

class User(object):
  def __init__(self, user_login):
    self.user_login = user_login
  
  meta = association_proxy('_metadict', 'meta_value', creator=UserMeta)

  def __repr__(self):
    return '<User(%r)>' % self.user_login

class Option(object):
  def __init__(self, option_name, option_value):
    self.option_name = option_name
    self.option_value = option_value

  def __repr__(self):
    return '<Option(%r, %r)>' % (self.option_name, self.option_value)

def init(prefix='wp'):
  metadata = MetaData()
  
  # tables
  terms = Table('%s_terms' % prefix, metadata,
    Column('term_id', Integer(), primary_key=True, nullable=False),
    Column('name', String(length=55), primary_key=False, nullable=False),
    Column('slug', String(length=200), primary_key=False, nullable=False),
    Column('term_group', Integer(), primary_key=False, nullable=False),
    UniqueConstraint('slug'),
  )
  
  term_taxonomy = Table('%s_term_taxonomy' % prefix, metadata,
    Column('term_taxonomy_id', Integer(), primary_key=True, nullable=False),
    Column('term_id', Integer(), primary_key=False, nullable=False),
    Column('taxonomy', String(length=32), primary_key=False, nullable=False),
    Column('description', Text(length=None), primary_key=False, nullable=False),
    Column('parent', Integer(), primary_key=False, nullable=False),
    Column('count', Integer(), primary_key=False, nullable=False),
    UniqueConstraint('term_id', 'taxonomy'),
    ForeignKeyConstraint(['term_id'], ['%s_terms.term_id' % prefix]),
    ForeignKeyConstraint(['parent'], ['%s_term_taxonomy.term_taxonomy_id' % prefix]),
  )

  term_relationships = Table('%s_term_relationships' % prefix, metadata,
    Column('object_id', Integer(), primary_key=True, nullable=False),
    Column('term_taxonomy_id', Integer(), primary_key=True, nullable=False),
    ForeignKeyConstraint(['term_taxonomy_id'], ['%s_term_taxonomy.term_taxonomy_id' % prefix]),
  )
  
  postmeta = Table('%s_postmeta' % prefix, metadata,
    Column('meta_id', Integer(), primary_key=True, nullable=False),
    Column('post_id', Integer(), primary_key=False, nullable=False),
    Column('meta_key', String(length=255), primary_key=False),
    Column('meta_value', Text(length=None), primary_key=False),
    ForeignKeyConstraint(['post_id'], ['%s_posts.ID' % prefix]),
  )
  
  posts = Table('%s_posts' % prefix, metadata,
    Column('ID', Integer(), primary_key=True, nullable=False),
    Column('post_author', Integer(), primary_key=False, nullable=False),
    Column('post_date', DateTime(timezone=False), primary_key=False, nullable=False),
    Column('post_date_gmt', DateTime(timezone=False), primary_key=False, nullable=False),
    Column('post_content', Text(length=None), primary_key=False, nullable=False),
    Column('post_title', Text(length=None), primary_key=False, nullable=False),
    Column('post_excerpt', Text(length=None), primary_key=False, nullable=False),
    Column('post_status', String(length=10), primary_key=False, nullable=False),
    Column('comment_status', String(length=15), primary_key=False, nullable=False),
    Column('ping_status', String(length=6), primary_key=False, nullable=False),
    Column('post_password', String(length=20), primary_key=False, nullable=False),
    Column('post_name', String(length=200), primary_key=False, nullable=False),
    Column('to_ping', Text(length=None), primary_key=False, nullable=False),
    Column('pinged', Text(length=None), primary_key=False, nullable=False),
    Column('post_modified', DateTime(timezone=False), primary_key=False, nullable=False),
    Column('post_modified_gmt', DateTime(timezone=False), primary_key=False, nullable=False),
    Column('post_content_filtered', Text(length=None), primary_key=False, nullable=False),
    Column('post_parent', Integer(), primary_key=False, nullable=False),
    Column('guid', String(length=255), primary_key=False, nullable=False),
    Column('menu_order', Integer(), primary_key=False, nullable=False),
    Column('post_type', String(length=20), primary_key=False, nullable=False),
    Column('post_mime_type', String(length=100), primary_key=False, nullable=False),
    Column('comment_count', Integer(), primary_key=False, nullable=False),
    ForeignKeyConstraint(['post_author'], ['%s_users.ID' % prefix]),
    ForeignKeyConstraint(['post_parent'], ['%s_posts.ID' % prefix]),
  )
  
  links = Table('%s_links' % prefix, metadata,
      Column('link_id', Integer(), primary_key=True, nullable=False),
      Column('link_url', String(length=255), primary_key=False, nullable=False),
      Column('link_name', String(length=255), primary_key=False, nullable=False),
      Column('link_image', String(length=255), primary_key=False, nullable=False),
      Column('link_target', String(length=25), primary_key=False, nullable=False),
      Column('link_category', Integer(), primary_key=False, nullable=False),
      Column('link_description', String(length=255), primary_key=False, nullable=False),
      Column('link_visible', String(length=1), primary_key=False, nullable=False),
      Column('link_owner', Integer(), primary_key=False, nullable=False),
      Column('link_rating', Integer(), primary_key=False, nullable=False),
      Column('link_updated', DateTime(timezone=False), primary_key=False, nullable=False),
      Column('link_rel', String(length=255), primary_key=False, nullable=False),
      Column('link_notes', Text(length=None), primary_key=False, nullable=False),
      Column('link_rss', String(length=255), primary_key=False, nullable=False),
      ForeignKeyConstraint(['link_owner'], ['%s_users.ID' % prefix]),
  )
  
  commentmeta = Table('%s_commentmeta' % prefix, metadata,
    Column('meta_id', Integer(), primary_key=True, nullable=False),
    Column('comment_id', Integer(), primary_key=False, nullable=False),
    Column('meta_key', String(length=255), primary_key=False),
    Column('meta_value', Text(length=None), primary_key=False),
    ForeignKeyConstraint(['comment_id'], ['%s_comments.comment_ID' % prefix]),
  )

  comments = Table('%s_comments' % prefix, metadata,
      Column('comment_ID', Integer(), primary_key=True, nullable=False),
      Column('comment_post_ID', Integer(), primary_key=False, nullable=False),
      Column('comment_author', Text(length=None), primary_key=False, nullable=False),
      Column('comment_author_email', String(length=100), primary_key=False, nullable=False),
      Column('comment_author_url', String(length=200), primary_key=False, nullable=False),
      Column('comment_author_IP', String(length=100), primary_key=False, nullable=False),
      Column('comment_date', DateTime(timezone=False), primary_key=False, nullable=False),
      Column('comment_date_gmt', DateTime(timezone=False), primary_key=False, nullable=False),
      Column('comment_content', Text(length=None), primary_key=False, nullable=False),
      Column('comment_karma', Integer(), primary_key=False, nullable=False),
      Column('comment_approved', String(length=4), primary_key=False, nullable=False),
      Column('comment_agent', String(length=255), primary_key=False, nullable=False),
      Column('comment_type', String(length=20), primary_key=False, nullable=False),
      Column('comment_parent', Integer(), primary_key=False, nullable=False),
      Column('user_id', Integer(), primary_key=False, nullable=False),
      ForeignKeyConstraint(['comment_post_ID'], ['%s_posts.ID' % prefix]),
      ForeignKeyConstraint(['comment_parent'], ['%s_comments.comment_ID' % prefix]),
      ForeignKeyConstraint(['user_id'], ['%s_users.ID' % prefix]),
  )
  
  usermeta = Table('%s_usermeta' % prefix, metadata,
    Column('umeta_id', Integer(), primary_key=True, nullable=False),
    Column('user_id', Integer(), primary_key=False, nullable=False),
    Column('meta_key', String(length=255), primary_key=False),
    Column('meta_value', Text(length=None), primary_key=False),
    ForeignKeyConstraint(['user_id'], ['%s_users.ID' % prefix]),
  )
    
  users = Table('%s_users' % prefix, metadata,
    Column('ID', Integer(), primary_key=True, nullable=False),
    Column('user_login', String(length=60), primary_key=False, nullable=False),
    Column('user_pass', String(length=64), primary_key=False, nullable=False),
    Column('user_nicename', String(length=50), primary_key=False, nullable=False),
    Column('user_email', String(length=100), primary_key=False, nullable=False),
    Column('user_url', String(length=100), primary_key=False, nullable=False),
    Column('user_registered', DateTime(timezone=False), primary_key=False, nullable=False),
    Column('user_activation_key', String(length=60), primary_key=False, nullable=False),
    Column('user_status', Integer(), primary_key=False, nullable=False),
    Column('display_name', String(length=250), primary_key=False, nullable=False),
  )

  options = Table('%s_options' % prefix, metadata,
    Column('option_id', Integer(), primary_key=True, nullable=False),
    Column('option_name', String(length=64), primary_key=True, nullable=False),
    Column('option_value', Text(length=None), primary_key=False, nullable=False),
    Column('autoload', String(length=3), primary_key=False, nullable=False),
  )
  
  # mappings
  mapper(Term, terms)
  taxonomy_mapper = mapper(
    Taxonomy,
    term_taxonomy,
    properties={'term': relation(Term)},
    polymorphic_on=term_taxonomy.c.taxonomy,
  )
  mapper(
    PostTag,
    properties={
      'posts': dynamic_loader(
        Post,
        secondary=term_relationships,
        primaryjoin=(term_taxonomy.c.term_taxonomy_id
             == term_relationships.c.term_taxonomy_id),
        secondaryjoin=(term_relationships.c.object_id
               == posts.c.ID),
        foreign_keys=[term_relationships.c.object_id,
              term_relationships.c.term_taxonomy_id],
      ),
    },
    inherits=taxonomy_mapper,
    polymorphic_identity='post_tag',
  )
  mapper(
    Category,
    properties={
      'children': relation(
        Category,
        backref=backref('parent_category',
                        remote_side=[term_taxonomy.c.term_taxonomy_id]),
      ),
      'posts': dynamic_loader(
        Post,
        secondary=term_relationships,
        primaryjoin=(term_taxonomy.c.term_taxonomy_id
                     == term_relationships.c.term_taxonomy_id),
        secondaryjoin=(term_relationships.c.object_id
                       == posts.c.ID),
        foreign_keys=[term_relationships.c.object_id,
                      term_relationships.c.term_taxonomy_id],
      ),
    },
    inherits=taxonomy_mapper,
    polymorphic_identity='category',
  )
  mapper(
    LinkCategory,
    properties={
      'links': relation(
        Link,
        secondary=term_relationships,
        primaryjoin=(term_taxonomy.c.term_taxonomy_id
                     == term_relationships.c.term_taxonomy_id),
        secondaryjoin=(term_relationships.c.object_id
                       == links.c.link_id),
        foreign_keys=[term_relationships.c.object_id,
                      term_relationships.c.term_taxonomy_id],
      ),
    },
    inherits=taxonomy_mapper,
    polymorphic_identity='link_category',
  )
  mapper(PostMeta, postmeta)
  mapper(
    Post,
    posts,
    properties={
      '_metadict': relation(PostMeta,
                            collection_class=column_mapped_collection(postmeta.c.meta_key)),
      'children': relation(
        Post,
        backref=backref('parent', remote_side=[posts.c.ID]),
      ),
      'post_tags': relation(
        PostTag,
        secondary=term_relationships,
        primaryjoin=(posts.c.ID
                     == term_relationships.c.object_id),
        secondaryjoin=(term_relationships.c.term_taxonomy_id
                       == term_taxonomy.c.term_taxonomy_id),
        foreign_keys=[term_relationships.c.object_id,
                      term_relationships.c.term_taxonomy_id],
      ),
      'categories': relation(
        Category,
        secondary=term_relationships,
        primaryjoin=(posts.c.ID
                     == term_relationships.c.object_id),
        secondaryjoin=(term_relationships.c.term_taxonomy_id
                       == term_taxonomy.c.term_taxonomy_id),
        foreign_keys=[term_relationships.c.object_id,
                      term_relationships.c.term_taxonomy_id],
      ),
      'comments': dynamic_loader(Comment, backref='post'),
    },
  )
  mapper(
      Link,
      links,
      properties={
        'categories': relation(
          LinkCategory,
          secondary=term_relationships,
          primaryjoin=(links.c.link_id
                       == term_relationships.c.object_id),
          secondaryjoin=(term_relationships.c.term_taxonomy_id
                         == term_taxonomy.c.term_taxonomy_id),
          foreign_keys=[term_relationships.c.object_id,
                        term_relationships.c.term_taxonomy_id],
        ),
      },
  )
  mapper(CommentMeta, commentmeta)
  mapper(
    Comment,
    comments,
    properties={
      '_metadict': relation(CommentMeta,
                            collection_class=column_mapped_collection(commentmeta.c.meta_key)),
      'children': relation(
        Comment,
        backref=backref('parent',
                        remote_side=[comments.c.comment_ID]),
      ),
    },
  )
  mapper(UserMeta, usermeta)
  mapper(
    User,
    users,
    properties={
        'metadata': relation(
            UserMeta,
            collection_class=column_mapped_collection(usermeta.c.meta_key),
        ),
        'posts': dynamic_loader(Post, backref='author'),
        'links': dynamic_loader(Link, backref='user'),
        'comments': dynamic_loader(Comment, backref='user'),
    },
  )
  mapper(Option, options)
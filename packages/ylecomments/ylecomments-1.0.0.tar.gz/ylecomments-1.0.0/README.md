# ylecomments v1

_Python package for fetching comments from Yle Comments API_

POSTing comments is not supported at this time. Support for this is unlikely.

## Installation

```bash
pip install ylecomments
```

## Example usage

```python
from ylecomments import ylecomments

# Get comments for a specific article
# https://yle.fi/a/74-20023410
article = ylecomments.YleArticle("74-20023410")
comments = article.get_approved_comments()

# Print the first comment
print(comments[0].content)

# Print the comment author's name
print(comments[0].author)

# Print the amount of likes the comment has
print(comments[0].likes)

# Other attributes:
# rejectedAt, children, content, likes, acceptedAt, createdByModerator,
# author, topicExternalId, id, parentId, topCommentId, authenticatedAuthor,
# topicId, createdAt, createdByTrustedCommentAuthor, createdByCommentator,
# isModerationReply
```

#
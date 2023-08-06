from datetime import datetime

import requests
from requests.utils import default_headers


class YleComment:
    """
    Object representing a Yle comment.

    Attributes:
        rejectedAt (str): Date and time when the comment was rejected. Seemingly always None.
        children (list): List of Comment objects that are replies to this comment.
        content (str): Comment content.
        likes (int): Number of likes the comment has received.
        acceptedAt (datetime): Date and time when the comment was accepted.
        createdByModerator (bool): Whether the comment was created by a moderator.
        author (str): Comment author.
        topicExternalId (str): External ID of the topic the comment belongs to.
        id (str): Comment ID.
        parentId (str): ID of the parent comment.
        topCommentId (str): In case the comment is a reply to a reply, this is the ID of the top-level comment.
        authenticatedAuthor (str): Some kind of user identifier.
        topicId (str): ID of the topic the comment belongs to.
        createdAt (datetime): Date and time when the comment was created.
        createdByTrustedCommentAuthor (bool): Whether the comment was created by a trusted comment author.
        createdByCommentator (bool): Whether the comment was created by a commentator.
        isModerationReply (bool): Whether the comment is a moderation reply.
    """

    def __init__(self, comment_json: dict) -> None:
        self.rejectedAt = comment_json.get("rejectedAt")
        self.children = [YleComment(child) for child in comment_json.get("children")]
        self.content = comment_json.get("content")
        self.likes = comment_json.get("likes")
        self.acceptedAt = datetime.fromisoformat(comment_json.get("acceptedAt"))
        self.createdByModerator = comment_json.get("createdByModerator")
        self.author = comment_json.get("author")
        self.topicExternalId = comment_json.get("topicExternalId")
        self.id = comment_json.get("id")
        self.parentId = comment_json.get("parentId")
        self.topCommentId = comment_json.get("topCommentId")
        self.authenticatedAuthor = comment_json.get("authenticatedAuthor")
        self.topicId = comment_json.get("topicId")
        self.createdAt = datetime.fromisoformat(comment_json.get("createdAt"))
        self.createdByTrustedCommentAuthor = comment_json.get("createdByTrustedCommentAuthor")
        self.createdByCommentator = comment_json.get("createdByCommentator")
        self.isModerationReply = comment_json.get("isModerationReply")

    def __repr__(self) -> str:
        return f"YleComment({self.id})"

    def __str__(self) -> str:
        return f"YleComment({self.id})"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class YleArticle:
    """
    Object representing a Yle article. get_approved_comments() to get a list of Comment objects.
    """

    def __init__(self,
                 article_id: str, ) -> None:
        self.article_id = article_id
        self.session = requests.Session()

    def get_approved_comments(
            self,
            app_id: str = "yle-comments-plugin",
            app_key: str = "sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D",
            order: str = "parent_created_at:asc",
            parent_limit: int = 10,
            max_hierarchy_depth: int = 2,
            from_parent_id: str = None,
            headers: str = requests.utils.default_headers()
    ) -> list:
        """
        Get approved comments for an article.

        Parameters:
            app_id (str): Application ID. Defaults to "yle-comments-plugin".
            app_key (str): Application key. Defaults to "sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D".
            order (str): Order of comments. Defaults to "parent_created_at:asc".
            parent_limit (int): Maximum number of comments to return. Defaults to 10.
            max_hierarchy_depth (int): Maximum depth of comment hierarchy. Defaults to 2.
            from_parent_id (str): ID of the parent comment to start from. Defaults to None.
            headers (str): Headers to use in the request. Defaults to requests.utils.default_headers().

        Returns:
            list: List of Comment objects.
        """
        url = f"https://comments.api.yle.fi/v1/topics/{self.article_id}/comments/accepted"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "order": order,
            "parent_limit": parent_limit,
            "max_hierarchy_depth": max_hierarchy_depth,
            "article_id": self.article_id,
            "from_parent_id": from_parent_id,
        }
        response = self.session.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return [YleComment(comment) for comment in response.json().get("data")]
        else:
            raise Exception(f"Yle Comments API returned status code {response.status_code}")

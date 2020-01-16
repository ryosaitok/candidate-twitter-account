class EvaluatedCandidate(object):

    def __init__(self, **kwargs):
        valid_keys = ["user_id",  # TwitterのユーザーID（不変）
                      "username",  # Twitterのユーザー名（可変）
                      "screen_name",  # Twitterのアカウント名（可変）
                      "profile",  # Twitterの自己紹介文（可変）
                      "job_category_possibility",  # 対象の職種である可能性（ex.エンジニア）
                      "career_type_possibility",  # 対象のキャリア種別の可能性（ex.21新卒）
                      "job_category_contribute_words",  # 職種の可能性判定対象となった単語とその%
                      "career_type_contribute_words"  # キャリア種別の可能性判定対象となった単語とその%
                      ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

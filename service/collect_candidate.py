# coding=utf-8
import tweepy
import os
from time import sleep
from service.google_sheet import google_sheet_api_service, sheet_service
from model.evaluated_candidate_model import EvaluatedCandidate

CANDIDATE_SHEET_NAME = '新卒採用候補者 収集アカウント'
USER_ID_COL_NUM = 1
ACCOUNT_NAME_COL_NUM = 4
SEARCH_TARGET_ACCOUNTS_SHEET_NAME = 'フォロー可能性高 アカウント'
TARGET_ACCOUNT_NAME_COL_NUM = 1
SEARCHED_DATETIME_COL_NUM = 3
WORDS_SHEET_NAME = '対象者 可能性高単語'
PERCENTAGE_COL_NUM = 1
JOB_CATEGORY_WORD_COL_NUM = 2
CAREER_TYPE_WORD_COL_NUM = 3

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
ANTISOCIAL_WORDS = os.environ['ANTISOCIAL_WORDS'].split(',')


def execute(gid):
    word_sheet = google_sheet_api_service.access_sheet(gid).worksheet(WORDS_SHEET_NAME)
    percentages = word_sheet.col_values(PERCENTAGE_COL_NUM)
    percentages.pop(0)
    percentages = [int(p) for p in percentages]

    job_csv_words = word_sheet.col_values(JOB_CATEGORY_WORD_COL_NUM)
    job_csv_words.pop(0)
    job_words = [w.split(',') for w in job_csv_words]
    job_words_dict = dict(zip(percentages, job_words))
    print('job_words_dict: {}'.format(job_words_dict))

    career_csv_words = word_sheet.col_values(CAREER_TYPE_WORD_COL_NUM)
    career_csv_words.pop(0)
    career_words = [w.split(',') for w in career_csv_words if w.strip() != '']
    career_words_dict = dict(zip(percentages, career_words))
    print('career_words_dict: {}'.format(career_words_dict))

    candidate_sheet = google_sheet_api_service.access_sheet(gid).worksheet(CANDIDATE_SHEET_NAME)
    user_ids = candidate_sheet.col_values(USER_ID_COL_NUM)
    user_ids.pop(0)
    user_ids = [int(u_i) for u_i in user_ids]

    target_sheet = google_sheet_api_service.access_sheet(gid).worksheet(SEARCH_TARGET_ACCOUNTS_SHEET_NAME)
    screen_names = target_sheet.col_values(TARGET_ACCOUNT_NAME_COL_NUM)
    screen_names.pop(0)
    searched_dt = target_sheet.col_values(SEARCHED_DATETIME_COL_NUM)
    searched_dt.pop(0)
    target_screen_name = screen_names[len(searched_dt)]

    api = prepare_twitter_api()

    # 検索対象アカウントがフォローしているアカウントに関して、可能性判定してSpread Sheetに記載していく
    friend_ids = api.friends_ids(screen_name=target_screen_name)
    # すでにSheetに記載済みのアカウントは判定対象外としたいのでリストから除く。
    target_ids = [f_id for f_id in friend_ids if f_id not in user_ids]
    print('検索対象@{}のフォローアカウント(判定済みは除く)の数:{}件（判定済={}件）\nAPIアクセス制限対策で10秒待ちます...'
          .format(target_screen_name, len(target_ids), len(friend_ids)-len(target_ids)))
    sleep(10)
    write_evaluated_users(gid, api, job_words_dict, career_words_dict, user_ids, target_ids)

    # 検索対象アカウントのフォロワーに関して、可能性判定してSpread Sheetに記載していく
    follower_ids = api.followers_ids(screen_name=target_screen_name)
    # すでにSheetに記載済みのアカウントは判定対象外としたいのでリストから除く（すでにフォローアカウントで見たIDは除外する）。
    target_ids = [f_id for f_id in follower_ids if f_id not in user_ids and f_id not in target_ids]
    print('検索対象@{}のフォロワーアカウント(判定済みは除く)の数:{}件（判定済={}件）\nAPIアクセス制限対策で10秒待ちます...'
          .format(target_screen_name, len(target_ids), len(follower_ids)-len(target_ids)))
    sleep(10)
    write_evaluated_users(gid, api, job_words_dict, career_words_dict, user_ids, target_ids)

    # ユーザー検索の元にしたアカウントが収集済みになった旨をSpread Sheetに記入します。
    print('Spread Sheetにアカウントの収集日時を書き込みます！')
    sheet_service.check_searched(gid, SEARCH_TARGET_ACCOUNTS_SHEET_NAME, len(searched_dt)+2, SEARCHED_DATETIME_COL_NUM)
    google_sheet_api_service.close_sheet()


def write_evaluated_users(gid, api, job_words_dict, career_words_dict, user_ids, target_ids):
    # ツイッターユーザーのユーザーID20件ずつのリスト（最大500件）にして、順次処理する。
    # フォロワー数が数万人の場合など処理時間が長くなってしまうため最大でも1000個になるよう絞っている。500件を扱う場合でも処理終了までに30分程度かかる見込み。
    ids_list = [target_ids[i:i + 20] for i in range(0, len(target_ids), 20)][:25]
    for i, ids in enumerate(ids_list):
        users = api.lookup_users(user_ids=ids)
        print('{}回目の処理開始。usersの数: {}\nAPIアクセス制限対策で10秒待ちます...'.format(i + 1, len(users)))
        sleep(10)

        targets = evaluate_candidate(api, job_words_dict, career_words_dict, user_ids, users)
        if len(targets) < 1:
            continue
        # 上限100ユーザー分の判定が終わった段階で取得できたアカウント情報をシートに書き込む。
        print('Spread Sheetに収集できたTwitterアカウントを書き込みます！')
        sheet_service.write_users(gid, CANDIDATE_SHEET_NAME, targets)


def evaluate_candidate(api, job_words_dict, career_words_dict, user_ids, users):
    targets = []
    for index, u in enumerate(users):
        screen_name = u.screen_name
        print('------\n{}/{}件目。アカウント名: {}の判定開始'.format(index + 1, len(users), screen_name))

        try:
            if u.id in user_ids or u.protected or is_antisocial([u.description]):
                print('判定対象外にしました。（Sheet記載済み or 鍵アカウント or プロフィールに反社会的な単語が含まる。）')
                continue

            tweet_texts = cursor_select_tweet_texts(api, user_id=u.id, cursor_count=3)
            print('APIアクセス制限対策で1秒待ちます...')
            sleep(1)
            if len(tweet_texts) < 1 or is_antisocial([u.description]) or is_antisocial(tweet_texts):
                print('判定対象外にしました。（ツイートが取得できなかったか、ツイートに反社会的な単語が含まれていた。）')
                continue

            job_possibility = 0
            job_possibility_words = []
            job_possibility_dict = evaluate_profile(u.description, job_words_dict)
            job_possibility += sum(job_possibility_dict.keys())
            job_possibility_words.extend(['{}:{}'.format(p, w) for p, w in job_possibility_dict.items()])

            career_possibility = 0
            career_possibility_words = []
            career_possibility_dict = evaluate_profile(u.description, career_words_dict)
            career_possibility += sum(career_possibility_dict.keys())
            career_possibility_words.extend(['{}:{}'.format(p, w) for p, w in career_possibility_dict.items()])

            job_possibility_dict = evaluate_tweets(tweet_texts, job_words_dict)
            job_possibility += sum(job_possibility_dict.keys())
            job_possibility_words.extend(['{}:{}'.format(p, w) for p, w in job_possibility_dict.items()])

            career_possibility_dict = evaluate_tweets(tweet_texts, career_words_dict)
            career_possibility += sum(career_possibility_dict.keys())
            career_possibility_words.extend(['{}:{}'.format(p, w) for p, w in career_possibility_dict.items()])

            if job_possibility <= 0 and career_possibility <= 0:
                print('【×】対象職種の可能性: {}%, 対象キャリア種別の可能性: {}%, '.format(job_possibility, career_possibility))
                continue

            print('【◯】対象職種の可能性: {}%, 対象キャリア種別の可能性: {}%, '.format(job_possibility, career_possibility))

            candidate = EvaluatedCandidate(user_id=u.id, username=u.name, screen_name=u.screen_name,
                                           profile=u.description, job_category_possibility=job_possibility,
                                           career_type_possibility=career_possibility,
                                           job_category_contribute_words=job_possibility_words,
                                           career_type_contribute_words=career_possibility_words)
            targets.append(candidate)
        except Exception as e:
            print(f'例外発生 e: {e}')
    return targets


def cursor_select_tweet_texts(api, user_id, cursor_count):
    """指定したユーザーのツイートをカーソル検索して取得する。0以下の場合は空のリストが返ります。"""
    count = 1
    min_id = -1
    tweet_texts = []
    try:
        while count <= cursor_count:
            if min_id == -1:
                tweets = api.user_timeline(user_id=user_id, trim_user=True, exclude_replies=True,
                                           include_rts=False)  # ユーザー情報・返信ツイート・リツイートは含まない)
                min_id = tweets[-1].id
                tweet_texts.extend([t.text for t in tweets])
            else:
                tweets = api.user_timeline(user_id=user_id, max_id=min_id, trim_user=True, exclude_replies=True,
                                           include_rts=False)  # 前回取得したツイート以降のツイートを取得する。ユーザー情報・返信ツイート・リツイートは含まない)
                if len(tweets) < 1:
                    break
                tweet_texts.extend([t.text for t in tweets])
            count += 1
            # TwitterAPIのリクエスト上限を考慮して最短でも1秒アクセス間隔をあける。
            sleep(1)
    except Exception as e:
        print(f'例外発生（鍵アカウントの場合に頻出）e: {e}')
    return tweet_texts


def evaluate_profile(profile, word_dict):
    output_dict = {}
    for percentage, words in word_dict.items():
        for word in words:
            if word in profile and word != '':
                print(f'対象単語: {word}, プロフ: {profile}')
                output_dict[percentage] = word
                break
    return output_dict


def evaluate_tweets(tweet_texts, word_dict):
    output_dict = {}
    is_next = False
    for percentage, words in word_dict.items():
        for text in tweet_texts:
            for word in words:
                if word in text and word != '':
                    print(f'対象単語: {word}, ツイート: {text}')
                    output_dict[percentage] = word
                    is_next = True
                    break
            if is_next:
                break
    return output_dict


def prepare_twitter_api():
    """TwitterのAPIアクセスキーを取得"""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def is_antisocial(texts):
    """反社会的な単語が含まれている文章が1件でもあればTrueを返します。"""
    for t in texts:
        for w in ANTISOCIAL_WORDS:
            if w in t:
                return True
    return False

from botoy import Action, FriendMsg, GroupMsg, EventMsg
from botoy import decorators as deco
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'USERsecretId'      # 替换为用户的 secretId(登录访问管理控制台获取)
secret_key = 'USERsecret_key'      # 替换为用户的 secretKey(登录访问管理控制台获取)
region = 'ap-where'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
bucketName= 'bucket-1234567' #替换为用户的储存桶名字
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


def receive_friend_msg(ctx: FriendMsg):
    Action(ctx.CurrentQQ)

@deco.ignore_botself
@deco.startswith("网盘搜索")
def receive_group_msg(ctx: GroupMsg):
    action= Action(ctx.CurrentQQ)
    keyWord = ctx.Content[4:]
    if keyWord == None:
        return 0
    response = client.list_objects(
    Bucket=bucketName,
    Prefix=''
    )
    print(response)
    for i in response['Contents']:
        if i['Key'].find(keyWord) != -1:
            fileUrl = client.get_object_url(
                Bucket=bucketName,
                Key=i['Key'],
                )
            action.uploadGroupFile(ctx.FromGroupId,fileUrl,fileName=i['Key'])


def receive_events(ctx: EventMsg):
    Action(ctx.CurrentQQ)

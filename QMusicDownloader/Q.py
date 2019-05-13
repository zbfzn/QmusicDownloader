import requests,json,warnings,base64
import requests;
from contextlib import closing

warnings.filterwarnings("ignore")
a,b,c=[],[],{}
def ab():
    a,b,c='',0,requests.get("http://lyfzn.top/vertify/api-Qmusic.php?key=***").text#联系开发者获取key
    cc=[]
    cc.append(c.split("\r\n")[0])
    cc.append(c.split("\r\n")[1])
    a=cc
    b=cc
    return cc
def ba():
    return ab()
b=ba()
def QPlay(qqnum):
    qqdata = requests.get(b[0].format(qqnum),verify=False)
    jsarr = json.loads(qqdata.text)
    status=jsarr['status']
    if not status:
        return False
    uin=jsarr['singer_uin']
    author = jsarr['singer_name']
    count = jsarr['count']
    desc = jsarr['message']
    shareUrl = jsarr['shareurl']
    data=jsarr['data']
    playlists_name = []
    playlists_id = []
    print("**账号详情**")
    print("创作人：{}\n账号：{}\n数目：{}\n描述：{}\n分享地址：{}".format(author,uin,count,desc,shareUrl))
    print("--"*20)
    print("**歌单列表**")
    for diss in data:
        playlists_name.append(diss['title'])
        playlists_id.append(diss['dissid'])
    playlist=dict(zip(playlists_name,playlists_id))
    i=0
    ids=[]
    for li in playlist:
        print("序号：{:<6}名称：{: <30}ID：{}".format(i,li,playlist[li]))
        ids.append(playlist[li])
        i+=1
    print("----" * 20)
    id=eval(input("输入歌单序号："))
    disstid=ids[id]
    mkdir("./downloads/{}/".format(disstid))
    downMusics(disstid)
    return True


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
         # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def downMusics(id):
    data=requests.get(b[1].format(id),verify=False)
    qqdata=json.loads(data.text)['data']
    print(json.dumps(qqdata,indent=True))
    num=1
    count=len(qqdata)
    for song in qqdata:
        types={'sizeape':"ape",'sizeflac':'flac','size320':'mp3','sizeogg':'ogg','size128':'mp3'}
        songname=song['songname']
        singername=song['singer_list'][0]['name']
        songtypes=song['songtypes']
        hasurl=False
        for ty in types:
            if songtypes[ty]['filesize']>0 and songtypes[ty]['urltype']==1:
                filename="{}-{}.{}".format(songname,singername,types[ty])
                path="./downloads/{}/{}".format(id,filename)
                download(songtypes[ty]['fileurl'],path,"{}/{}".format(num,count))
                print("{}下载成功".format(filename))
                hasurl=True
                break
        if not hasurl:
            filename = "{}-{}.{}".format(songname, singername, "mp3")
            path = "./downloads/{}/{}".format(id, filename)
            download(songtypes['size128']['fileurl'], path,"{}/{}".format(num,count))
            print("{}下载成功".format(filename))
        num+=1


class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

def download(url,path,tag):
    #要下载文件的地址
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        progress = ProgressBar("razorback<{}>".format(tag), total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        # chunk_size = chunk_size < content_size and chunk_size or content_size
        # 你将要保存文件的位置和名字
        with open(path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


qqnum=input("输入解析的QQ号：")
QPlay(qqnum)

import binascii
import zlib
import os

repository = "C:/Users/Ulquiorra/test"


def read_git_object(git_file: str):
    global repository

    folder = git_file[:2]
    name = git_file[2:]

    filename = repository+"/.git/objects/"+folder+"/"+name

    with open(filename, "rb") as file:
        raw_data = file.read()
    data = zlib.decompress(raw_data)

    _type, contents = data.split(b'\x00', maxsplit=1)[0:2]
    _type = _type.decode().split()[0]
    _contents = None
    if _type in ["blob", "commit"]:
        _contents = contents.decode()
    elif _type == "tree":
        _contents = list()
        while contents != b'':
            filemode, contents = contents.split(b' ', maxsplit=1)
            filename, contents = contents.split(b'\x00', maxsplit=1)
            sha1, contents = contents[:20], contents[20:]
            filemode = filemode.decode()
            filename = filename.decode()
            sha1 = binascii.hexlify(sha1).decode()
            _contents.append((filemode, filename, sha1))
    return _type, _contents


def read_heads(heads_name: str):
    global repository
    filename = f"{repository}/.git/refs/heads/{heads_name}"

    with open(filename, "rb") as file:
        data = file.read()
    contents = data.split(b'\x00', maxsplit=1)[0].decode()

    return contents


def ptree(e, hash,n):
    # print(" "*n)
    # print()
    # print(" "*n,"tree "+hash, end='->')
    for i in e[1]:
        if i[0] == '100644':
            print(" " * n, "tree " + hash, end='->')
            print(i[2])
        else:
            # print(e)
            print(" " * n, "tree " + hash, end='->')
            print("tree " +i[2])
            ptree(read_git_object(i[2]),i[2],n*2)

    return

def prcomm(content,n):
    content_split = content[1].split(maxsplit=4)
    parent_name = content[1].split('\n')[-2]
    print(parent_name)

    # for

    if content_split[0] == 'tree':
        tree = read_git_object(content_split[1])
        print(" "*n,parent_name,"-> tree",content_split[1])

        ptree(tree,content_split[1],n*2)

    if content_split[2] == 'parent':
        parent_commit = content_split[3]
        parent_commit_name = content[1].split('\n')[-2]
        print(" "*n,parent_commit_name,end="->")
        prcomm(read_git_object(parent_commit), n * 2)
    else:
        return None
    return read_git_object(parent_commit)




branch = 'master'
if os.path.exists(repository):
    last_commit = read_heads(branch)[:-1]
    content = read_git_object(last_commit)
    print(" content ",content)
    while (content!=None):
        content=prcomm(content,1)
        print("____________________________________")

# C:/Users/Ulquiorra/test
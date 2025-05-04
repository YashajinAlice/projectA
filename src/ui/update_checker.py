import requests
from packaging import version

def check_for_updates():
    """
    检查GitHub上是否有更新
    返回: (是否有更新, 新版本号, 更新公告)
    """
    # 当前版本
    current_version = "1.0.0"
    
    try:
        # GitHub 仓库信息
        github_repo = "YashajinAlice/projectA"
        github_branch = "main"  # 分支名稱（默認為 main）

        # 调用 GitHub API 获取最新版本信息
        api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()  # 如果请求失败会抛出异常
        
        data = response.json()
        remote_version = data["tag_name"].lstrip("v")  # 去掉版本号前的 "v"
        
        # 检查是否有更新
        has_update = version.parse(remote_version) > version.parse(current_version)
        
        return (has_update, remote_version, data["body"])
    
    except Exception as e:
        print(f"检查更新时出错: {e}")
        raise
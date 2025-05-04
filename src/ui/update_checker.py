import os
import requests
from packaging import version

def check_for_updates():
    """
    检查GitHub上是否有更新并自动更新文件
    """
    # 当前版本
    current_version = "1.0.3"
    
    try:
        # GitHub 仓库信息
        github_repo = "YashajinAlice/projectA"

        # 调用 GitHub API 获取最新版本信息
        api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()  # 如果请求失败会抛出异常
        
        data = response.json()
        remote_version = data["tag_name"].lstrip("v")  # 去掉版本号前的 "v"
        
        # 检查是否有更新
        if version.parse(remote_version) > version.parse(current_version):
            print(f"发现新版本: {remote_version}")
            print(f"更新内容: {data['body']}")

            # 下载更新清单
            manifest_url = f"https://raw.githubusercontent.com/{github_repo}/main/update_manifest.json"
            download_and_update_files(manifest_url)

            print("更新完成，请重新启动应用程序以应用更改。")
        else:
            print("当前已是最新版本。")
    
    except Exception as e:
        print(f"检查更新时出错: {e}")
        raise


def download_and_update_files(manifest_url):
    """
    根据更新清单下载并更新文件
    :param manifest_url: 更新清单的 URL
    """
    try:
        # 下载更新清单
        response = requests.get(manifest_url)
        response.raise_for_status()
        manifest = response.json()

        # 遍历清单中的文件
        for file_info in manifest.get("files", []):
            file_path = file_info["path"]
            file_url = file_info["url"]

            # 创建本地目录
            local_path = os.path.join(os.path.dirname(__file__), "..", file_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # 下载文件
            print(f"正在下载文件: {file_path}...")
            file_response = requests.get(file_url)
            file_response.raise_for_status()

            # 保存文件
            with open(local_path, "wb") as f:
                f.write(file_response.content)
            print(f"文件已更新: {file_path}")

        print("所有文件已成功更新！")

    except Exception as e:
        print(f"更新文件时出错: {e}")